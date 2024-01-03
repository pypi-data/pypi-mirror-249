import unittest
from infinite_relations import *


# UTILS
def compare_relation_members(r1: Relation, r2: Relation, c: int) -> bool:
    """Compare first x tuples, or all"""
    return compare_lists_orderless(
        r1.get_schema(), r2.get_schema()
    ) and compare_lists_orderless(r1.list_members(c), r2.list_members(c))


# CONSTANTS
naturals = integer_relation()
odds = general_integer_relation(["n"], lambda n: n % 2 == 1)
evens = general_integer_relation(["n"], lambda n: n % 2 == 0)

add_schema = ["x", "y", "sum"]
raw_add = general_integer_relation(add_schema, add_cond)


# Test basic relational operations
class BasicOperationsTest(unittest.TestCase):
    def test_union(self):
        result = union(evens, odds)
        expected = naturals

        self.assertTrue(compare_relation_members(result, expected, 20))

    def test_difference(self):
        result = difference(naturals, odds)
        expected = evens

        self.assertTrue(compare_relation_members(result, expected, 20))

    def test_cross_join(self):
        r1 = list_relation(
            ["name", "age"],
            [
                {"name": "Dani", "age": 23},
                {"name": "Emil", "age": 26},
                {"name": "Franta", "age": 25},
            ],
        )
        r2 = general_integer_relation(["round"], lambda x: x > 0)

        result = cross_join(r1, r2)
        expected = list_relation(
            ["round", "name", "age"],
            [
                {"round": 1, "name": "Dani", "age": 23},
                {"round": 1, "name": "Emil", "age": 26},
                {"round": 1, "name": "Franta", "age": 25},
                {"round": 2, "name": "Dani", "age": 23},
                {"round": 2, "name": "Emil", "age": 26},
                {"round": 2, "name": "Franta", "age": 25},
                {"round": 3, "name": "Dani", "age": 23},
                {"round": 3, "name": "Emil", "age": 26},
                {"round": 3, "name": "Franta", "age": 25},
                {"round": 4, "name": "Dani", "age": 23},
            ],
        )

        self.assertTrue(compare_relation_members(result, expected, 10))

    def test_projection(self):
        r = general_integer_relation(["x", "y", "z"], empty_cond)

        result = projection(r, ["x", "y"])
        expected = general_integer_relation(["x", "y"], empty_cond)

        self.assertTrue(compare_relation_members(result, expected, 20))

    def test_selection(self):
        result = selection(naturals, lambda n: n < 10)
        expected = list_relation(
            ["n"],
            [
                {"n": 0},
                {"n": 1},
                {"n": 2},
                {"n": 3},
                {"n": 4},
                {"n": 5},
                {"n": 6},
                {"n": 7},
                {"n": 8},
                {"n": 9},
            ],
        )

        self.assertTrue(compare_relation_members(result, expected, 10))


# Test operations derived from basic ones
class DerivedOperationsTest(unittest.TestCase):
    def test_intersection(self):
        result = intersection(naturals, evens)

        self.assertTrue(compare_relation_members(result, evens, 20))

    def test_natural_join(self):
        r1 = list_relation(
            ["name", "english_mark", "math_mark"],
            [
                {"name": "Dani", "english_mark": 90, "math_mark": 85},
                {"name": "Emil", "english_mark": 52, "math_mark": 99},
                {"name": "Franta", "english_mark": 70, "math_mark": 65},
            ],
        )

        result = natural_join(
            r1, add_relation(["english_mark", "math_mark", "mark_sum"])
        )
        expected = list_relation(
            ["name", "english_mark", "math_mark", "mark_sum"],
            [
                {"name": "Dani", "english_mark": 90, "math_mark": 85, "mark_sum": 175},
                {"name": "Emil", "english_mark": 52, "math_mark": 99, "mark_sum": 151},
                {
                    "name": "Franta",
                    "english_mark": 70,
                    "math_mark": 65,
                    "mark_sum": 135,
                },
            ],
        )

        self.assertTrue(compare_relation_members(result, expected, 3))

    def test_division(self):
        return
        r1 = general_integer_relation(["num"], empty_cond)
        r2 = list_relation(["char"], [{"char": "a"}, {"char": "b"}, {"char": "c"}])
        r3 = cross_join(r1, r2)
        r4 = list_relation(
            ["num", "char"], [{"num": 2, "char": "b"}, {"num": 3, "char": "c"}]
        )
        r5 = difference(r3, r4)

        result = division(r5, r2)
        expected = list_relation(
            ["num"],
            [
                {"num": 1},
                {"num": 4},
                {"num": 5},
                {"num": 6},
                {"num": 7},
            ],
        )

        self.assertTrue(compare_relation_members(result, expected, 5))
