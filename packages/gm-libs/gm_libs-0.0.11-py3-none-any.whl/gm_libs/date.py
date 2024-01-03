# coding=utf-8
from __future__ import print_function, absolute_import
import datetime as dt


# 获取去年时间（day 大于本月最后一天时，取本月最后一天）
def l_get_last_year(now: dt.datetime, day: int = 0):
    now.replace(year=now.year - 1)

    return now


# 获取上个季度时间（day 大于本月最后一天时，取本月最后一天）
def l_get_last_season(now: dt.datetime, day: int = 0):
    now = l_get_last_month(now, day)
    now = l_get_last_month(now, day)
    now = l_get_last_month(now, day)

    return now


# 获取上月时间（day 大于本月最后一天时，取本月最后一天）
def l_get_last_month(now: dt.datetime, day: int = 0):
    result = now.replace(day=1) - dt.timedelta(days=1)

    if day == 0:
        day = now.day
    max_day = get_month_max_day(now.year, now.month)
    if max_day < day:
        day = max_day

    result.replace(day)
    return result


# 获取当月最大天数
def get_month_max_day(year: int, month: int):
    if (month == 2) and ((year % 4 == 0) or ((year % 100 == 0) and (year % 400 == 0))):
        return 29
    elif month == 2:
        return 28
    elif month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        return 31
    else:
        return 30
