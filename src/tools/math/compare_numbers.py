# compare_module.py

from typing import Union

def is_equal(a: Union[int, float], b: Union[int, float]) -> bool:
    """
    두 수가 같은지 비교합니다.
    
    Args:
        a (Union[int, float]): 첫 번째 수
        b (Union[int, float]): 두 번째 수
    
    Returns:
        bool: 두 수가 같으면 True, 아니면 False
    """
    return a == b

def is_greater(a: Union[int, float], b: Union[int, float]) -> bool:
    """
    첫 번째 수가 두 번째 수보다 큰지 비교합니다.
    
    Args:
        a (Union[int, float]): 첫 번째 수
        b (Union[int, float]): 두 번째 수
    
    Returns:
        bool: 첫 번째 수가 두 번째 수보다 크면 True, 아니면 False
    """
    return a > b

def is_less(a: Union[int, float], b: Union[int, float]) -> bool:
    """
    첫 번째 수가 두 번째 수보다 작은지 비교합니다.
    
    Args:
        a (Union[int, float]): 첫 번째 수
        b (Union[int, float]): 두 번째 수
    
    Returns:
        bool: 첫 번째 수가 두 번째 수보다 작으면 True, 아니면 False
    """
    return a < b

def is_greater_or_equal(a: Union[int, float], b: Union[int, float]) -> bool:
    """
    첫 번째 수가 두 번째 수보다 크거나 같은지 비교합니다.
    
    Args:
        a (Union[int, float]): 첫 번째 수
        b (Union[int, float]): 두 번째 수
    
    Returns:
        bool: 첫 번째 수가 두 번째 수보다 크거나 같으면 True, 아니면 False
    """
    return a >= b

def is_less_or_equal(a: Union[int, float], b: Union[int, float]) -> bool:
    """
    첫 번째 수가 두 번째 수보다 작거나 같은지 비교합니다.
    
    Args:
        a (Union[int, float]): 첫 번째 수
        b (Union[int, float]): 두 번째 수
    
    Returns:
        bool: 첫 번째 수가 두 번째 수보다 작거나 같으면 True, 아니면 False
    """
    return a <= b
