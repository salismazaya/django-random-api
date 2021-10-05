from django.utils.timezone import deactivate


TOTAL_DAYS_OF_MONTH = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}

def get_total_days_of_month(datetime):
    month = int(datetime.strftime('%m'))
    year = int(datetime.strftime('%Y'))
    total_days = TOTAL_DAYS_OF_MONTH[month]
    if month == 2 and year % 4 == 0 and year % 100 == 0 and year % 400 == 0:
        total_days += 1
    
    return total_days
