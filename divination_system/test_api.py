# -*- coding: utf-8 -*-
"""API 冒烟测试：python -m pytest test_api.py 或直接 python test_api.py"""
from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_bazi():
    r = client.post("/api/v1/bazi", json={"birth_datetime": "1995-08-16T14:30:00"})
    assert r.status_code == 200
    data = r.json()["data"]
    assert data["pillars"] == {"年柱": "乙亥", "月柱": "甲申", "日柱": "己卯", "时柱": "辛未"}
    assert data["shengxiao"] == "猪"


def test_iching_time_and_coins():
    r = client.post("/api/v1/iching/cast",
                    json={"method": "time", "moment": "2026-07-04T10:00:00",
                          "question_number": 8})
    assert r.status_code == 200
    assert r.json()["data"]["name"]  # 卦名非空
    r2 = client.post("/api/v1/iching/cast", json={"method": "coins"})
    assert r2.status_code == 200
    assert 1 <= r2.json()["data"]["moving_line"] <= 6


def test_astrology():
    r = client.get("/api/v1/astrology", params={"birth_date": "1995-08-16"})
    assert r.status_code == 200
    assert r.json()["data"]["name"] == "狮子座"


def test_personality():
    r = client.get("/api/v1/personality/questions")
    assert r.status_code == 200 and len(r.json()["data"]) == 8
    r2 = client.post("/api/v1/personality/score",
                     json={"blood_type": "A",
                           "answers": ["B", "A", "B", "B", "A", "A", "A", "A"]})
    assert r2.status_code == 200
    assert r2.json()["data"]["mbti"]["type"] == "ENTJ"


def test_report_full_and_validation():
    payload = {"name": "测试缘主", "birth_datetime": "1995-08-16T14:30:00",
               "blood_type": "A",
               "answers": ["B", "A", "B", "B", "A", "A", "A", "A"]}
    r = client.post("/api/v1/report", json=payload)
    assert r.status_code == 200
    data = r.json()["data"]
    assert set(data["scores"]) == {"事业运", "财富运", "感情运", "健康运"}
    assert "四柱" in data["report_markdown"]
    # 支持直接传 MBTI 类型
    r2 = client.post("/api/v1/report", json={
        "name": "测试缘主", "birth_datetime": "1995-08-16T14:30:00",
        "blood_type": "O", "mbti_type": "INFP"})
    assert r2.status_code == 200
    # answers 与 mbti_type 均缺失 → 422
    r3 = client.post("/api/v1/report", json={
        "name": "x", "birth_datetime": "1995-08-16T14:30:00", "blood_type": "O"})
    assert r3.status_code == 422


if __name__ == "__main__":
    for fn in [v for k, v in sorted(globals().items()) if k.startswith("test_")]:
        fn()
        print(f"PASS {fn.__name__}")
    print("全部测试通过 ✔")
