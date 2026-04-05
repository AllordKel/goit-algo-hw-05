from typing import Callable
from decimal import Decimal
from re import findall


def generator_numbers(text: str):
    """
    Generator that produces all real numbers separated by tabs from the text using regular expressions.
    Decimal used to avoid faults in further calculations.
    """
    pattern = r" \d+\.?\d* "  # pattern collects possible fractions, all number should be separated by spaces due to requirements/documentation.
    nums = findall(pattern, text)
    for i in range(len(nums)):
        yield Decimal(nums[i])


def sum_profit(text: str, func: Callable):
    """
    Function that uses generator to return total income
    """
    return sum(func(text))