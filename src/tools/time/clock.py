import datetime

datetime.timezone(datetime.timedelta(hours=9))
"""
설명:
이 파일은 현재 시간을 알 수 있는 함수들을 모아놓은 파일입니다.
"""
def time_now():
    """
    설명:
    현재 시간을 %H:%M:%S 형식으로 반환합니다.
    """
    return datetime.datetime.now().strftime("%H:%M:%S")

def hour_now():
    """
    설명:
    지금이 몇시인지 반환합니다.
    """
    return datetime.datetime.now().strftime("%H")

def minute_now():
    """
    설명:
    지금이 몇분인지 반환합니다.
    """
    return datetime.datetime.now().strftime("%M")

def second_now():
    """
    설명:
    지금이 몇초인지 반환합니다.
    """
    return datetime.datetime.now().strftime("%S")