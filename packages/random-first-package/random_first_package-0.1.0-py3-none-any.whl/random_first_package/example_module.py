"""Random Package Example Module"""
from typing import Union
import math

def calculate_circle_area(radius: Union[int, float]) -> float:
    """Calculate the area of a circle"""
    return math.pi * radius ** 2

if __name__ == "__main__":
    print(calculate_circle_area(5))
