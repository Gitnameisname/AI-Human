import datetime

def time_now():
    """
    현재 시간을 %H:%M:%S 형식으로 반환합니다.
    """
    return datetime.datetime.now().strftime("%H:%M:%S")

def hour_now():
    """
    지금이 몇시인지 반환합니다.
    """
    return datetime.datetime.now().strftime("%H")

def minute_now():
    """
    지금이 몇분인지 반환합니다.
    """
    return datetime.datetime.now().strftime("%M")

def second_now():
    """
    지금이 몇초인지 반환합니다.
    """
    return datetime.datetime.now().strftime("%S")