import math
from typing import Union

def integrate_power(a: Union[int, float], b: Union[int, float], n: Union[int, float]) -> float:
    """
    a부터 b까지 x의 n승을 적분하는 함수입니다.

    Args:
        a (Union[int, float]): 적분 구간의 시작값
        b (Union[int, float]): 적분 구간의 끝값
        n (Union[int, float]): x의 거듭제곱 (x^n)

    Returns:
        float: a부터 b까지 x^n을 적분한 값
    """
    if n == -1:
        # x^(-1)의 적분은 ln(x)이므로 특수한 경우 처리
        return math.log(b) - math.log(a)
    else:
        return (b**(n+1) - a**(n+1)) / (n+1)
