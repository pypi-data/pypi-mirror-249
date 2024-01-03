"""Boolean functions to be used when creating selections
"""


def equality_cond(x: object, y: object) -> bool:
    return x == y


def add_cond(x: int, y: int, sum: int) -> bool:
    return x + y == sum


def empty_cond(*any) -> bool:
    return True
