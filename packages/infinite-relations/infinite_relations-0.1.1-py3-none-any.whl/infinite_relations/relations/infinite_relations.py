from ..utils.list_operations import dict_from_lists
from ..utils.relational_schema import RelationalSchema
from .relation import Relation
from ..relations.list_relation import ListRelation
from ..operations.selection import Selection
from ..operations.cross_join import CrossJoin
from inspect import getfullargspec
import itertools
import re


class IntegerRelation(Relation):
    """Unary relation containing all non-negative integers"""

    def __init__(self, schema: list = ["n"]):
        """Creates unary integer relation with a given one-attribute schema

        Parameters
        ----------
        schema : list
            Relational schema with one attribute, by default ["n"]

        Raises
        ------
        Exception
            If schema doesn't have exactly 1 attribute
        """
        if len(schema) == 1:
            super().__init__(schema)
        else:
            raise Exception("Schema of IntegerRelation must have 1 attribute")

    def can_be_infinite(self):
        return True

    def can_is_member_loop(self):
        return False

    def members(self):
        """Yields an infinite sequence of non-negative integers in order"""
        i = 0
        while True:
            yield dict_from_lists(self.get_schema(), [i])
            i += 1

    def is_member(self, tpl: dict):
        if not super().can_be_member(tpl):
            return False
        val = list(tpl.values())[0]
        return isinstance(val, int) and val >= 0


class GeneralIntegerRelation(Selection):
    """Infinite relation containing integer tuples which satisfy a given condition"""

    def __init__(self, schema: list, condition: callable):
        """Creates an infinite relation of integer tuples determined by a given schema and condition

        Parameters
        ----------
        schema : list
            A list of attribute names
        condition : callable
            Condition that tuples must satisfy

        Raises
        ------
        Exception
            If length of schema doesn't match number of condition parameters
        """
        len_cond_params = len(getfullargspec(condition).args)
        if len_cond_params != len(schema) and len_cond_params != 0:
            raise Exception("Schema length must match number of condition parameters")

        if len(schema) == 0:
            result = ListRelation([])
        else:
            result = IntegerRelation([schema[0]])
            for attr in schema[1:]:
                result = CrossJoin(result, IntegerRelation([attr]))
        super().__init__(result, condition, schema)

    def can_be_infinite(self):
        return True

    def can_is_member_loop(self):
        return False


class AddRelation(Relation):
    """Ternary relation containing all possible sums of non-negative integers"""

    def __init__(self, schema):
        """Creates an add relation with a given schema

        Parameters
        ----------
        schema : RelationalSchema, optional
            Relational schema

        Raises
        ------
        Exception
            If length of schema is not 3
        """
        if len(schema) == 3:
            super().__init__(schema)
        else:
            raise Exception("Schema of AddRelation must have 3 attributes")

    def can_be_infinite(self):
        return True

    def can_is_member_loop(self):
        return False

    def members(self):
        """Yields all possible triplets of numbers where x + y == z"""
        i = 0
        while True:
            for j in range(i + 1):
                yield dict_from_lists(self.get_schema(), [j, i - j, i])
            i += 1

    def is_member(self, tpl: dict) -> bool:
        if not super().can_be_member(tpl):
            return False
        vals = list(tpl.values())
        for val in vals:
            if not isinstance(val, int):
                return False
        return vals[0] + vals[1] == vals[2]


class FibonacciRelation(Relation):
    """Unary relation containing all members of the fibonacci sequence"""

    def __init__(self):
        """Creates unary relation containing the fibonacci sequence"""
        super().__init__(["fib"])

    def members(self):
        """Generates the fibonacci sequence"""
        f1 = 0
        f2 = 1
        while True:
            yield dict_from_lists(self.get_schema(), [f1])
            f1, f2 = f2, f1 + f2


class EqualRelation(Relation):
    """Binary integer relation where every tuple consists of two equal numbers"""

    def __init__(self, schema: list = ["x", "y"]):
        """Creates binary relation of equal numbers"""
        if not len(schema) == 2:
            raise Exception("Schema of EqualRelation must have 2 attributes")
        super().__init__(schema)

    def can_is_member_loop(self) -> bool:
        return False

    def is_member(self, tpl: dict) -> bool:
        if not super().can_be_member(tpl):
            return False
        vals = list(tpl.values())
        for val in vals:
            if not isinstance(val, int):
                return False
        return vals[0] == vals[1]

    def members(self):
        """Yields tuples of two equal integers"""
        i = 0
        while True:
            yield dict_from_lists(self.get_schema(), [i, i])
            i += 1


class UnequalRelation(Relation):
    """Binary integer relation where every tuple consists of two unequal numbers"""

    def __init__(self):
        """Creates binary relation of unequal numbers"""
        super().__init__(["lesser", "greater"])

    def can_is_member_loop(self) -> bool:
        return False

    def is_member(self, tpl: dict) -> bool:
        if not super().can_be_member(tpl):
            return False
        vals = list(tpl.values())
        for val in vals:
            if not isinstance(val, int):
                return False
        return vals[0] < vals[1]

    def members(self):
        """Yields tuples of two equal integers"""
        i = 0
        while True:
            for j in range(i):
                yield dict_from_lists(self.get_schema(), [j, i])
            i += 1


class WordRelation(Relation):
    """Relation of all possible combinations of the standard 26 letters of the alphabet (lowercase),
    starting from one-letter words and getting longer.
    """

    alphabet = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]

    def __init__(self, schema: list = ["word"]):
        """Creates relation of all possible words"""
        if not len(schema) == 1:
            raise Exception("Schema of WordRelation must have 1 attributes")
        super().__init__(schema)

    def can_is_member_loop(self) -> bool:
        return False

    def is_member(self, tpl: dict) -> bool:
        if not super().can_be_member(tpl):
            return False
        val = list(tpl.values())[0]
        return re.fullmatch(val, r"[a-z]+")

    def members(self):
        """Yields all possible words"""
        i = 0
        while True:
            for combination in itertools.product(self.alphabet, repeat=i):
                yield dict_from_lists(self.get_schema(), ["".join(combination)])
            i += 1
