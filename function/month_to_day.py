def is_leap_month(lap_year) -> bool:
    """
    盼端該年二月是否為閏月
    :param lap_year: 輸入年份
    :return: True 或者 False
    """
    # 如果該年份可以被4整除但是不被100整除，或者可以被400整除，那麼該年份的2月為閏月
    return (lap_year % 100 != 0 and lap_year % 4 == 0) or lap_year % 400 == 0


def month_to_day(lap_year_input, month_input):
    """
    判斷某年某月總共有幾天
    :param lap_year_input: 年份
    :param month_input: 月份
    :return:
    """
    month_input = int(month_input)  # 將月份轉換為整數
    lap_year = int(lap_year_input)  # 將年份轉換為整數

    if month_input == 1:
        return 31
    elif month_input == 2:
        is_leap = is_leap_month(lap_year)  # 判斷該年二月是否為閏月
        if is_leap:
            return 29
        else:
            return 28
    elif month_input == 3:
        return 31
    elif month_input == 4:
        return 30
    elif month_input == 5:
        return 31
    elif month_input == 6:
        return 30
    elif month_input == 7:
        return 31
    elif month_input == 8:
        return 31
    elif month_input == 9:
        return 30
    elif month_input == 10:
        return 31
    elif month_input == 11:
        return 30
    elif month_input == 12:
        return 31
