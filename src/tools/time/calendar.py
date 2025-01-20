import datetime

def date_today():
    """
    오늘 날짜를 %Y-%m-%d 형식으로 반환합니다.
    """
    return datetime.datetime.now().strftime("%Y-%m-%d")

def year_today():
    """
    올해가 몇년인지 반환합니다.
    """
    return datetime.datetime.now().strftime("%Y")

def month_today():
    """
    이번 달이 몇월인지 반환합니다.
    """
    return datetime.datetime.now().strftime("%m")

def day_today():
    """
    오늘이 며칠인지 반환합니다.
    """
    return datetime.datetime.now().strftime("%d")

def weekday_today():
    """
    오늘이 무슨 요일인지 반환합니다.
    """
    return datetime.datetime.now().strftime("%A")

