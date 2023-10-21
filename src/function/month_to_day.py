def is_leap_month(year: int) -> int:
    """
    盼端該年二月是否為閏月
    :param year: 輸入年份
    :return: True 或者 False
    """
    # 如果該年份可以被4整除但是不被100整除，或者可以被400整除，那麼該年份的2月為閏月
    return 1 if (year % 4 == 0) and (year % 100 != 0 or year % 400 == 0) else 0


def month_to_day(lap_year_input, month_input):
    """
    判斷某年某月總共有幾天
    :param lap_year_input: 年份
    :param month_input: 月份
    :return:
    """
    monthDays = [
        [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
        [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    ]
    month_input = int(month_input)  # 將月份轉換為整數
    lap_year = int(lap_year_input)  # 將年份轉換為整數
    is_leap = is_leap_month(lap_year)
    return monthDays[is_leap][month_input - 1]
