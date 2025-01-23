from typing import Union

def sum(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    이 함수는 두 수를 더하는 함수입니다.

    Args:
        a (Union[int, float]): 첫 번째 숫자
        b (Union[int, float]): 두 번째 숫자

    Returns:
        Union[int, float]: 두 수의 합
    """
    return a + b

def substraction(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    이 함수는 두 수를 빼는 함수입니다.

    Args:
        a (Union[int, float]): 첫 번째 숫자
        b (Union[int, float]): 두 번째 숫자

    Returns:
        Union[int, float]: 두 수의 차
    """
    return a - b

def multiplication(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    이 함수는 두 수를 곱하는 함수입니다.

    Args:
        a (Union[int, float]): 첫 번째 숫자
        b (Union[int, float]): 두 번째 숫자

    Returns:
        Union[int, float]: 두 수의 곱
    """
    return a * b

def division(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    이 함수는 두 수를 나누는 함수입니다.

    Args:
        a (Union[int, float]): 첫 번째 숫자
        b (Union[int, float]): 두 번째 숫자

    Returns:
        Union[int, float]: 두 수의 나눈 값
    """
    if b == 0:
        return "Error: Division by zero"
    return a / b