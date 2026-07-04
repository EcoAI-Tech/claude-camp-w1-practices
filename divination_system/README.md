# 天机阁 · 智能命理系统（MVP）

融合**周易八卦、四柱八字、星座、血型 + MBTI 人格测评**的算卦系统产品原型。

- 📄 完整的产品设计与商业化方案见 [`PRODUCT_DESIGN.md`](PRODUCT_DESIGN.md)
- 🐍 纯 Python 3 标准库实现，无第三方依赖

## 快速开始

```bash
cd divination_system
python main.py --demo   # 一键生成样例报告
python main.py          # 交互模式：输入生辰、血型、答题、起卦
```

报告会打印到终端并保存为 `report_<姓名>.md`。

## 模块一览

| 文件 | 说明 |
|---|---|
| `bazi.py` | 八字四柱排盘、五行旺缺与补益建议 |
| `iching.py` | 梅花易数时间卦 / 金钱课摇卦，64 卦断语 + 动爻提示 |
| `astrology.py` | 太阳星座、元素属性、幸运色/数字 |
| `personality.py` | 血型性格 + 8 题 MBTI 快测 |
| `report.py` | 四体系加权融合，四维运势评分（确定性可复现） |
| `main.py` | CLI 入口 |

> 免责声明：本项目属传统文化与编程练习，所有测算结果仅供娱乐参考，
> 不构成任何医疗、投资或人生决策依据。
