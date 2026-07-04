# -*- coding: utf-8 -*-
"""「天机阁」智能命理系统 — FastAPI 服务层

启动：
    uvicorn api:app --host 0.0.0.0 --port 8000

交互式文档：http://localhost:8000/docs

对应 PRODUCT_DESIGN.md 中的技术架构：本服务即"测算规则引擎"的服务化，
商业版在其前面加 API 网关（鉴权/限流/计费），在其后接 LLM 解读服务。
"""
from datetime import date, datetime
from typing import List, Literal, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from astrology import get_sign
from bazi import WUXING_ADVICE, compute_bazi
from iching import cast_by_coins, cast_by_time
from personality import (BLOOD_TRAITS, MBTI_BRIEF, QUESTIONS, blood_profile,
                         mbti_profile, score_mbti)
from report import build_report

DISCLAIMER = "本接口结果基于传统文化与心理测评，仅供娱乐与自我探索参考，不构成任何决策依据。"

app = FastAPI(
    title="天机阁 · 智能命理系统 API",
    description="融合周易八卦、四柱八字、星座、血型+MBTI 的测算规则引擎（MVP）。"
                + DISCLAIMER,
    version="0.1.0",
)


# ---------- 请求/响应模型 ----------

class BaziRequest(BaseModel):
    birth_datetime: datetime = Field(..., description="出生日期时间，如 1995-08-16T14:30:00")


class IChingRequest(BaseModel):
    method: Literal["time", "coins"] = Field("time", description="time=梅花易数时间卦，coins=金钱课摇卦")
    question_number: int = Field(0, ge=0, le=99, description="求测者报数（仅时间卦使用），增强参与感")
    moment: Optional[datetime] = Field(None, description="起卦时刻，缺省为服务器当前时间（仅时间卦使用）")


class PersonalityRequest(BaseModel):
    blood_type: Literal["A", "B", "O", "AB"] = "O"
    answers: List[Literal["A", "B"]] = Field(..., min_length=8, max_length=8,
                                             description="8 题快测答案，按题目顺序")


class ReportRequest(BaseModel):
    name: str = Field("缘主", max_length=32)
    birth_datetime: datetime
    blood_type: Literal["A", "B", "O", "AB"] = "O"
    answers: Optional[List[Literal["A", "B"]]] = Field(
        None, min_length=8, max_length=8, description="8 题快测答案；与 mbti_type 二选一")
    mbti_type: Optional[str] = Field(None, description="已知 MBTI 类型（如 ENTJ）；与 answers 二选一")
    cast_method: Literal["time", "coins"] = "time"
    question_number: int = Field(0, ge=0, le=99)

    @field_validator("mbti_type")
    @classmethod
    def _check_mbti(cls, v):
        if v is not None and v.upper() not in MBTI_BRIEF:
            raise ValueError(f"未知的 MBTI 类型: {v}")
        return v


# ---------- 单项测算接口 ----------

@app.get("/health")
def health():
    return {"status": "ok", "service": "tianjige-engine", "version": app.version}


@app.post("/api/v1/bazi", summary="八字排盘")
def bazi_endpoint(req: BaziRequest):
    result = compute_bazi(req.birth_datetime)
    advice_key = (result["lacking"][0] if result["lacking"][0] != "无"
                  else result["day_master_wuxing"])
    return {"data": {**result, "advice": WUXING_ADVICE[advice_key]},
            "disclaimer": DISCLAIMER}


@app.post("/api/v1/iching/cast", summary="周易起卦")
def iching_endpoint(req: IChingRequest):
    if req.method == "coins":
        result = cast_by_coins()
    else:
        result = cast_by_time(req.moment or datetime.now(), req.question_number)
    return {"data": result, "disclaimer": DISCLAIMER}


@app.get("/api/v1/astrology", summary="星座画像")
def astrology_endpoint(birth_date: date):
    return {"data": get_sign(birth_date), "disclaimer": DISCLAIMER}


@app.get("/api/v1/personality/questions", summary="获取人格快测题目")
def questions_endpoint():
    return {"data": [{"index": i + 1, "question": q} for i, (q, *_ ) in enumerate(QUESTIONS)],
            "blood_types": list(BLOOD_TRAITS)}


@app.post("/api/v1/personality/score", summary="人格测评计分")
def personality_endpoint(req: PersonalityRequest):
    mbti = score_mbti(req.answers)
    return {"data": {"blood": blood_profile(req.blood_type),
                     "mbti": mbti_profile(mbti)},
            "disclaimer": DISCLAIMER}


# ---------- 融合报告（核心付费接口） ----------

@app.post("/api/v1/report", summary="四体系融合报告")
def report_endpoint(req: ReportRequest):
    if req.answers is None and req.mbti_type is None:
        raise HTTPException(status_code=422, detail="answers 与 mbti_type 至少提供一项")

    bazi_r = compute_bazi(req.birth_datetime)
    sign = get_sign(req.birth_datetime.date())
    blood_p = blood_profile(req.blood_type)
    mbti_p = mbti_profile(req.mbti_type or score_mbti(req.answers))
    if req.cast_method == "coins":
        hexagram = cast_by_coins()
    else:
        hexagram = cast_by_time(datetime.now(), req.question_number)

    markdown, scores = build_report(req.name, req.birth_datetime, bazi_r,
                                    hexagram, sign, blood_p, mbti_p)
    return {
        "data": {
            "scores": scores,
            "bazi": bazi_r,
            "hexagram": hexagram,
            "astrology": sign,
            "blood": blood_p,
            "mbti": mbti_p,
            "report_markdown": markdown,
        },
        "disclaimer": DISCLAIMER,
    }
