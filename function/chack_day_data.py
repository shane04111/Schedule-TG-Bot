from my_time import get_current_year, get_current_month, get_current_day

time_year = get_current_year()
time_month = get_current_month()
time_day = get_current_day()


def check_day_data(year, month, day):
    if int(year) == int(time_year) and int(month) == int(time_month) and int(day) == int(time_day):
        return True
    else:
        return False
