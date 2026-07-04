# -*- coding: utf-8 -*-
"""融合报告引擎：把八字、卦象、星座、血型/MBTI 四路结果加权融合，
生成结构化的个人命理报告（Markdown 文本）。

评分为确定性算法（同一人同一天结果一致），这是付费产品建立
"准"感与复购信任的关键——绝不能每次刷新分数都变。
"""
import hashlib
from datetime import datetime

DIMENSIONS = ["事业运", "财富运", "感情运", "健康运"]

# 各维度受哪个五行主导（示意规则，商业版由命理顾问校准规则库）
DIM_WUXING = {"事业运": "木", "财富运": "金", "感情运": "火", "健康运": "土"}


def _seed_score(key: str, low=58, high=97) -> int:
    """由输入内容哈希出稳定分数，保证结果可复现。"""
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return low + int(digest[:8], 16) % (high - low + 1)


def build_report(name, birth: datetime, bazi_r, hexagram, sign, blood, mbti,
                 today=None):
    today = today or datetime.now()
    day_key = today.strftime("%Y-%m-%d")

    lines = []
    lines.append(f"# {name} 的天机综合报告")
    lines.append(f"\n> 生成日期：{day_key} ｜ 本报告基于传统文化与心理测评，"
                 f"仅供娱乐与自我探索参考，不构成任何决策依据。\n")

    # 一、八字命盘
    p = bazi_r["pillars"]
    lines.append("## 一、八字命盘")
    lines.append(f"- 四柱：{p['年柱']}年 {p['月柱']}月 {p['日柱']}日 {p['时柱']}时"
                 f"（属{bazi_r['shengxiao']}）")
    lines.append(f"- 日主：{bazi_r['day_master']}（{bazi_r['day_master_wuxing']}），"
                 f"五行分布：" + "、".join(f"{k}{v}" for k, v in bazi_r["wuxing_counts"].items()))
    lines.append(f"- 五行最旺：{bazi_r['dominant']}；所缺：{'、'.join(bazi_r['lacking'])}")
    from bazi import WUXING_ADVICE
    advice_key = bazi_r["lacking"][0] if bazi_r["lacking"][0] != "无" else bazi_r["day_master_wuxing"]
    lines.append(f"- 补益建议：{WUXING_ADVICE[advice_key]}")

    # 二、周易卦象
    lines.append("\n## 二、本次求测卦象")
    lines.append(f"- 起卦：{hexagram['method']}，上卦{hexagram['upper']}，下卦{hexagram['lower']}")
    lines.append(f"- 得【{hexagram['name']}】：{hexagram['judgment']}")
    lines.append(f"- {hexagram['line_hint']}")

    # 三、星座
    lines.append("\n## 三、星座画像")
    lines.append(f"- 太阳{sign['name']}（{sign['element']}象）：{sign['traits']}")
    lines.append(f"- {sign['element_note']}")
    lines.append(f"- 幸运色：{sign['lucky_color']} ｜ 幸运数字：{sign['lucky_number']}")

    # 四、血型 × MBTI
    lines.append("\n## 四、性格底色（血型 × MBTI）")
    lines.append(f"- 血型 {blood['type']} 型｜{blood['title']}：{blood['desc']}")
    lines.append(f"- MBTI {mbti['type']}｜{mbti['brief']}")

    # 五、四维运势评分（确定性融合）
    lines.append(f"\n## 五、今日四维运势（{day_key}）")
    base = f"{name}|{birth.isoformat()}|{blood['type']}|{mbti['type']}|{day_key}"
    scores = {}
    for dim in DIMENSIONS:
        s = _seed_score(base + dim)
        # 卦象吉断语微调 + 五行契合微调
        if any(w in hexagram["judgment"] for w in ("吉", "成", "赢", "泰", "升")):
            s = min(99, s + 2)
        if DIM_WUXING[dim] == bazi_r["dominant"]:
            s = min(99, s + 3)
        if DIM_WUXING[dim] in bazi_r["lacking"]:
            s = max(50, s - 3)
        scores[dim] = s
        bar = "█" * (s // 10) + "░" * (10 - s // 10)
        lines.append(f"- {dim}：{s} 分 {bar}")

    best = max(scores, key=scores.get)
    weakest = min(scores, key=scores.get)
    lines.append(f"\n**综合解读**：今日 {best} 最旺，宜将主要精力投入相关事项；"
                 f"{weakest} 偏弱，涉及事宜宜守不宜攻。卦得【{hexagram['name']}】，"
                 f"{hexagram['judgment']}结合你 {mbti['type']} 的行事风格与"
                 f"{blood['type']} 型血的{blood['title'][:2]}特质，"
                 f"建议：先谋后动，把幸运数字 {sign['lucky_number']} 当作今日的行动锚点。")

    lines.append("\n---\n*本报告由「天机阁」智能命理引擎生成，内容属传统文化娱乐范畴。*")
    return "\n".join(lines), scores
