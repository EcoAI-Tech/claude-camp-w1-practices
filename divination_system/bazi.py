# -*- coding: utf-8 -*-
"""八字排盘引擎（简化版）

以 1949-10-01（甲子日）为锚点推算日柱；年柱以立春（约2月4日）为界，
月柱以十二节气近似日期为界。精确到分钟的真太阳时校正不在 MVP 范围内，
商业版应接入天文历法库（如 sxtwl）。
"""
from datetime import date, datetime

GAN = "甲乙丙丁戊己庚辛壬癸"
ZHI = "子丑寅卯辰巳午未申酉戌亥"
SHENGXIAO = "鼠牛虎兔龙蛇马羊猴鸡狗猪"

# 天干/地支对应五行
GAN_WUXING = dict(zip(GAN, "木木火火土土金金水水"))
ZHI_WUXING = dict(zip(ZHI, "水土木木土火火土金金土水"))

# 各月节气（近似日期）：立春后为寅月(索引0)
JIEQI_APPROX = [(2, 4), (3, 6), (4, 5), (5, 6), (6, 6), (7, 7),
                (8, 8), (9, 8), (10, 8), (11, 7), (12, 7), (1, 6)]

ANCHOR = date(1949, 10, 1)  # 甲子日


def _ganzhi(index):
    return GAN[index % 10] + ZHI[index % 12]


def year_pillar(d):
    """年柱，以立春为界。"""
    year = d.year
    if (d.month, d.day) < (2, 4):
        year -= 1
    return _ganzhi(year - 4), year


def month_pillar(d, year_gan_index):
    """月柱：先定节气月序（0=寅月），再按'五虎遁'起月干。"""
    md = (d.month, d.day)
    if md >= (2, 4):
        # 立春(2/4)至大雪(12/7)之间：取最后一个已过的节气（不含次年小寒）
        month_index = 0
        for i, boundary in enumerate(JIEQI_APPROX[:11]):
            if md >= boundary:
                month_index = i
    else:
        # 1月至立春前：小寒(1/6)后为丑月，否则仍是子月
        month_index = 11 if md >= (1, 6) else 10
    # 甲己之年丙作首：月干 = 年干组别*2 + 2 + 月序
    gan_i = (year_gan_index % 5) * 2 + 2 + month_index
    zhi_i = (month_index + 2) % 12  # 寅=2
    return GAN[gan_i % 10] + ZHI[zhi_i]


def day_pillar(d):
    offset = (d - ANCHOR).days
    return _ganzhi(offset % 60), offset % 60


def hour_pillar(hour, day_gan_index):
    """时柱：'五鼠遁'——甲己日起甲子时。23点起算次日子时（此处简化为当日）。"""
    zhi_i = ((hour + 1) // 2) % 12
    gan_i = ((day_gan_index % 5) * 2 + zhi_i) % 10
    return GAN[gan_i] + ZHI[zhi_i]


def compute_bazi(birth: datetime):
    """返回八字四柱及五行统计。"""
    d = birth.date()
    yp, adj_year = year_pillar(d)
    mp = month_pillar(d, GAN.index(yp[0]))
    dp, day_index = day_pillar(d)
    hp = hour_pillar(birth.hour, day_index % 10)

    pillars = [yp, mp, dp, hp]
    counts = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
    for p in pillars:
        counts[GAN_WUXING[p[0]]] += 1
        counts[ZHI_WUXING[p[1]]] += 1

    day_master = dp[0]
    lacking = [e for e, c in counts.items() if c == 0]
    dominant = max(counts, key=counts.get)
    return {
        "pillars": {"年柱": yp, "月柱": mp, "日柱": dp, "时柱": hp},
        "shengxiao": SHENGXIAO[(adj_year - 4) % 12],
        "day_master": day_master,
        "day_master_wuxing": GAN_WUXING[day_master],
        "wuxing_counts": counts,
        "dominant": dominant,
        "lacking": lacking or ["无"],
    }


WUXING_ADVICE = {
    "金": "宜从事金融、法务、精密制造等『金』性行业，佩戴金属饰品，多用白色调。",
    "木": "宜从事教育、文创、医疗健康等『木』性行业，多接触绿植与自然，用青绿色调。",
    "水": "宜从事贸易、物流、传媒等流动性强的『水』性行业，近水而居更聚财，用蓝黑色调。",
    "火": "宜从事互联网、能源、餐饮等『火』性行业，保持热情与曝光度，用红色调提运。",
    "土": "宜从事地产、农业、行政管理等『土』性行业，稳扎稳打积累资产，用黄色调。",
}
