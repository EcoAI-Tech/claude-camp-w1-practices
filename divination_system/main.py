# -*- coding: utf-8 -*-
"""「天机阁」智能命理系统 — CLI 演示入口

用法：
    python main.py            # 交互模式：逐步输入信息并答题
    python main.py --demo     # 演示模式：使用内置样例数据直接出报告
"""
import sys
from datetime import datetime

from astrology import get_sign
from bazi import compute_bazi
from iching import cast_by_time, cast_by_coins
from personality import QUESTIONS, blood_profile, mbti_profile, score_mbti
from report import build_report


def collect_interactive():
    print("=" * 46)
    print("  天机阁 · 智能命理系统（MVP 演示版）")
    print("=" * 46)
    name = input("请输入姓名/昵称：").strip() or "缘主"
    raw = input("请输入出生日期时间（如 1995-08-16 14:30）：").strip()
    birth = datetime.strptime(raw, "%Y-%m-%d %H:%M")
    blood = input("请输入血型（A/B/O/AB）：").strip() or "O"

    print("\n—— 人格快测（8 题，输入 A 或 B）——")
    answers = []
    for i, (q, *_ ) in enumerate(QUESTIONS, 1):
        ans = ""
        while ans not in ("A", "B"):
            ans = input(f"{i}. {q}\n   你的选择：").strip().upper()
        answers.append(ans)

    method = input("\n起卦方式：1=时间起卦(默认) 2=摇卦：").strip()
    lucky = input("报一个 1-99 的数字（用于起卦，可回车跳过）：").strip()
    number = int(lucky) if lucky.isdigit() else 0
    hexagram = cast_by_coins() if method == "2" else cast_by_time(datetime.now(), number)
    return name, birth, blood, answers, hexagram


def demo_inputs():
    name = "示例缘主"
    birth = datetime(1995, 8, 16, 14, 30)
    blood = "A"
    answers = ["B", "A", "B", "B", "A", "A", "A", "A"]  # -> ENTJ
    hexagram = cast_by_time(datetime(2026, 7, 4, 10, 0), question_number=8)
    return name, birth, blood, answers, hexagram


def main():
    if "--demo" in sys.argv:
        name, birth, blood, answers, hexagram = demo_inputs()
    else:
        name, birth, blood, answers, hexagram = collect_interactive()

    bazi_r = compute_bazi(birth)
    sign = get_sign(birth.date())
    blood_p = blood_profile(blood)
    mbti_p = mbti_profile(score_mbti(answers))

    text, _scores = build_report(name, birth, bazi_r, hexagram, sign, blood_p, mbti_p)
    print("\n" + text)

    out = f"report_{name}.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"\n[已保存报告：{out}]")


if __name__ == "__main__":
    main()
