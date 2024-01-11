import calendar


def month_to_day(year: int, month: int) -> int:
    """
    判斷某年某月總共有幾天
    :param year: 年份
    :param month: 月份
    :return:
    """
    month_days = [
        [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
        [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    ]
    if 0 > month < 12:
        raise calendar.IllegalMonthError(month)
    is_leap = calendar.isleap(year)
    return month_days[is_leap][month - 1]
