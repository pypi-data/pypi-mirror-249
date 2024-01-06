# -*- coding:utf-8 -*-
from parse_datetime import parse_ymd, parse_duration


def run(func, dt, default_empty=False):
    print("{}('{}'): {}".format(func.__name__, dt, func(dt, default_empty=default_empty)))


def test_parse_ymd():
    print()
    run(parse_ymd, "")
    run(parse_ymd, "最近")

    run(parse_ymd, "当天")
    run(parse_ymd, "昨天")
    run(parse_ymd, "5号")
    run(parse_ymd, "前天")

    run(parse_ymd, "本周")
    run(parse_ymd, "上周")
    run(parse_ymd, "本 周")

    run(parse_ymd, "当月")
    run(parse_ymd, "12月")
    run(parse_ymd, "1月")
    run(parse_ymd, "上月")
    run(parse_ymd, "最近一个月")
    run(parse_ymd, "这 个 月 ")
    run(parse_ymd, "1季度")
    run(parse_ymd, "2季度")

    run(parse_ymd, "本季度")
    run(parse_ymd, "上季度")

    run(parse_ymd, "今年")
    run(parse_ymd, "去年")

    run(parse_ymd, "5月2号")
    run(parse_ymd, "2023-04-01,2023-04-30")
    run(parse_ymd, "去年6月")
    run(parse_ymd, "今年3月")
    run(parse_ymd, "2022年")
    run(parse_ymd, "昨天早上")

    run(parse_ymd, "28号到29号", True)
    run(parse_ymd, "", True)
    run(parse_ymd, "上个月28号到29号", True)
    run(parse_ymd, "上个月28号", True)
    run(parse_ymd, "到29号", True)


def test_parse_duration():
    assert parse_duration("1个半小时") == 5400
    assert parse_duration("30 分钟") == 1800
    assert parse_duration("10秒钟") == 10
    assert parse_duration("1天又6个小时") == 108000
