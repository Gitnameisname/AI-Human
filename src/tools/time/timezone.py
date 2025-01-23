import os, time
from datetime import datetime

def timezone_now():
    """
    현재 TimeZone을 확인합니다.
    """
    return datetime.now().astimezone().tzname()
    
def change_timezone(target_timezone: str):
    """
    TimeZone을 target_timezone으로 변경합니다.

    Args:
        target_timezone (str): 변경할 TimeZone (예시: "Asia/Seoul", "UTC", "America/New_York", ...)

    Returns:
        timezone_str: 변경된 TimeZone 문자열
    """
    os.environ['TZ'] = target_timezone
    time.tzset()
    timezone_str = timezone_now()
    return timezone_str
