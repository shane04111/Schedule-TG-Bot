from datetime import datetime


def time_datetime():
    """
    :return: 當前時間(datetime格式)
    """
    return datetime.now()


def time_date():
    """
    :return: 當前時間(date格式)
    """
    return datetime.now().date()


def time_time():
    """
    :return: 當前時間(time格式)
    """
    return datetime.now().time()


def time_year():
    """
    :return: 當前年份
    """
    return datetime.now().year


def time_month():
    """
    :return: 當前月份
    """
    return datetime.now().month


def time_day():
    """
    :return: 當前日期
    """
    return datetime.now().day


def time_hour():
    """
    :return: 當前時間
    """
    return datetime.now().hour


def time_minute():
    """
    :return: 當前分鐘
    """
    return datetime.now().minute


def time_second():
    """
    :return: 當前秒數
    """
    return datetime.now().second
