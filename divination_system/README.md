# 天机阁 · 智能命理系统（MVP）

融合**周易八卦、四柱八字、星座、血型 + MBTI 人格测评**的算卦系统产品原型。

- 📄 完整的产品设计与商业化方案见 [`PRODUCT_DESIGN.md`](PRODUCT_DESIGN.md)
- 🐍 测算引擎为纯 Python 3 标准库实现；API 服务层基于 FastAPI

## 快速开始（CLI，零依赖）

```bash
cd divination_system
python main.py --demo   # 一键生成样例报告
python main.py          # 交互模式：输入生辰、血型、答题、起卦
```

报告会打印到终端并保存为 `report_<姓名>.md`。

## API 服务（FastAPI）

```bash
pip install -r requirements.txt
uvicorn api:app --host 0.0.0.0 --port 8000
# 交互式文档：http://localhost:8000/docs
python test_api.py      # 冒烟测试
```

| 接口 | 方法 | 说明 |
|---|---|---|
| `/health` | GET | 健康检查 |
| `/api/v1/bazi` | POST | 八字排盘 + 五行分析 |
| `/api/v1/iching/cast` | POST | 起卦（时间卦/摇卦） |
| `/api/v1/astrology` | GET | 星座画像 |
| `/api/v1/personality/questions` | GET | 获取 8 题快测题目 |
| `/api/v1/personality/score` | POST | 血型 + MBTI 计分 |
| `/api/v1/report` | POST | **四体系融合报告（核心付费接口）** |

融合报告示例：

```bash
curl -X POST http://localhost:8000/api/v1/report \
  -H 'Content-Type: application/json' \
  -d '{"name":"缘主","birth_datetime":"1995-08-16T14:30:00",
       "blood_type":"A","mbti_type":"ENTJ"}'
```

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
