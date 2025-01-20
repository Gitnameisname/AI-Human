import datetime

"""
설명:
이 파일은 오늘 날짜와 관련된 함수들을 모아놓은 파일입니다.
"""

def date_today():
    """
    설명:
    오늘 날짜를 %Y-%m-%d 형식으로 반환합니다.
    """
    return datetime.datetime.now().strftime("%Y-%m-%d")

def year_today():
    """
    설명:
    올해가 몇년인지 반환합니다.
    """
    return datetime.datetime.now().strftime("%Y")

def month_today():
    """
    설명:
    이번 달이 몇월인지 반환합니다.
    """
    return datetime.datetime.now().strftime("%m")

def day_today():
    """
    설명:
    오늘이 며칠인지 반환합니다.
    """
    return datetime.datetime.now().strftime("%d")

def weekday_today():
    """
    설명:
    오늘이 무슨 요일인지 반환합니다.
    """
    return datetime.datetime.now().strftime("%A")

