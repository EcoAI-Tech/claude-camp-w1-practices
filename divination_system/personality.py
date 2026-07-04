# -*- coding: utf-8 -*-
"""血型性格 + 简版 MBTI 人格测试引擎。

MBTI 采用 8 题快测（每维度 2 题），商业版应替换为 93 题标准量表
或接入持证咨询师复核，报告中须注明测评仅供参考。
"""

BLOOD_TRAITS = {
    "A": ("谨慎完美型", "细腻敏感、责任感强，适合深耕专业；注意别把压力都憋在心里。"),
    "B": ("自由创意型", "乐观随性、创造力强，适合创意与开拓工作；注意坚持与收尾。"),
    "O": ("目标行动型", "自信果断、领导力强，适合带队攻坚；注意倾听与耐心。"),
    "AB": ("理性双面型", "冷静客观、兼具理性与感性，适合分析策划；注意主动表达情感。"),
}

# 8 题：每题 (题干, 选A计入的字母, 选B计入的字母)
QUESTIONS = [
    ("聚会结束后你通常感觉？  A.充电了，还想续摊  B.被掏空，想独处回血", "E", "I"),
    ("认识新朋友时你更倾向？  A.主动开启话题  B.等对方先开口", "E", "I"),
    ("做决定时你更相信？  A.已验证的经验和事实  B.直觉和未来的可能性", "S", "N"),
    ("读书时你更关注？  A.具体情节和细节  B.背后的寓意和联想", "S", "N"),
    ("朋友向你倾诉时你先？  A.分析问题给方案  B.安抚情绪表共情", "T", "F"),
    ("评价一件事你更看重？  A.对错与效率  B.感受与和谐", "T", "F"),
    ("旅行前你会？  A.做好详细攻略  B.说走就走随缘玩", "J", "P"),
    ("面对截止日期你通常？  A.提前完成  B.压哨冲刺", "J", "P"),
]

MBTI_BRIEF = {
    "INTJ": "建筑师·战略布局", "INTP": "逻辑学家·理性探索",
    "ENTJ": "指挥官·果断统帅", "ENTP": "辩论家·机变创新",
    "INFJ": "提倡者·理想引路", "INFP": "调停者·温柔坚定",
    "ENFJ": "主人公·感召众人", "ENFP": "竞选者·热情洋溢",
    "ISTJ": "物流师·严谨可靠", "ISFJ": "守卫者·细心守护",
    "ESTJ": "总经理·执行有力", "ESFJ": "执政官·热心周到",
    "ISTP": "鉴赏家·冷静实干", "ISFP": "探险家·随性审美",
    "ESTP": "企业家·敢闯敢拼", "ESFP": "表演者·活力四射",
}


def score_mbti(answers):
    """answers: 长度为 8 的 'A'/'B' 序列 -> MBTI 四字母类型。"""
    tally = {}
    for (_, a_letter, b_letter), ans in zip(QUESTIONS, answers):
        letter = a_letter if ans.upper() == "A" else b_letter
        tally[letter] = tally.get(letter, 0) + 1
    mbti = ""
    for pair in ("EI", "SN", "TF", "JP"):
        a, b = pair
        mbti += a if tally.get(a, 0) >= tally.get(b, 0) else b
    return mbti


def blood_profile(blood_type):
    key = blood_type.upper()
    title, desc = BLOOD_TRAITS.get(key, BLOOD_TRAITS["O"])
    return {"type": key if key in BLOOD_TRAITS else "O", "title": title, "desc": desc}


def mbti_profile(mbti):
    mbti = mbti.upper()
    return {"type": mbti, "brief": MBTI_BRIEF.get(mbti, "独特型·自成一派")}
