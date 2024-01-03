import unittest
from infinite_relations import *


# UTILS
def compare_relation_members(r1: Relation, r2: Relation) -> bool:
    """Compare first x tuples, or all"""
    return compare_lists_orderless(
        r1.get_schema(), r2.get_schema()
    ) and compare_lists_orderless(r1.list_members(), r2.list_members())


# CONSTANTS
schema = ["name", "age"]
names = ["Dani", "Emil", "Franta", "Martin", "Karel", "Standa", "Rudolf", "Tereza"]
ages = [23, 26, 25, 23, 28, 19, 25, 14]


# Test basic relational operations
class BasicOperationsTest(unittest.TestCase):
    def test_union(self):
        r1 = list_relation(
            schema,
            [{"name": name, "age": age} for (name, age) in zip(names[:5], ages[:5])],
        )
        r2 = list_relation(
            schema,
            [{"name": name, "age": age} for (name, age) in zip(names[3:8], ages[3:8])],
        )

        result = union(r1, r2)
        expected = list_relation(
            schema, [{"name": name, "age": age} for (name, age) in zip(names, ages)]
        )

        self.assertTrue(compare_relation_members(result, expected))

    def test_difference(self):
        r1 = list_relation(
            schema,
            [{"name": name, "age": age} for (name, age) in zip(names[:5], ages[:5])],
        )
        r2 = list_relation(
            schema,
            [{"name": name, "age": age} for (name, age) in zip(names[3:8], ages[3:8])],
        )

        result = difference(r1, r2)
        expected = list_relation(
            schema,
            [{"name": name, "age": age} for (name, age) in zip(names[:3], ages[:3])],
        )

        self.assertTrue(compare_relation_members(result, expected))

    def test_cross_join(self):
        r1 = list_relation(
            ["name", "age"],
            [{"name": name, "age": age} for (name, age) in zip(names[:3], ages[:3])],
        )
        r2 = list_relation(["round"], [{"round": 1}, {"round": 2}, {"round": 3}])

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
            ],
        )

        self.assertTrue(compare_relation_members(result, expected))

    def test_projection(self):
        r = list_relation(
            ["name", "age"],
            [{"name": name, "age": age} for (name, age) in zip(names, ages)],
        )

        result = projection(r, ["name"])
        expected = list_relation(["name"], [{"name": name} for name in names])

        self.assertTrue(compare_relation_members(result, expected))

    def test_selection(self):
        r = list_relation(
            ["name", "age"],
            [{"name": name, "age": age} for (name, age) in zip(names, ages)],
        )

        result = selection(r, lambda age: age > 25, ["age"])
        expected = list_relation(
            ["name", "age"],
            [{"name": "Emil", "age": 26}, {"name": "Karel", "age": 28}],
        )

        self.assertTrue(compare_relation_members(result, expected))


# Test operations derived from basic ones
class DerivedOperationsTest(unittest.TestCase):

    def test_intersection(self):
        r1 = list_relation(
            schema,
            [{"name": name, "age": age} for (name, age) in zip(names[:5], ages[:5])],
        )
        r2 = list_relation(
            schema,
            [{"name": name, "age": age} for (name, age) in zip(names[3:8], ages[3:8])],
        )

        result = intersection(r1, r2)
        expected = list_relation(
            schema, [{"name": "Martin", "age": 23}, {"name": "Karel", "age": 28}]
        )

        self.assertTrue(compare_relation_members(result, expected))

    def test_natural_join(self):
        r1 = list_relation(
            ["id"] + schema,
            [
                {"id": i + 1, "name": name, "age": age}
                for (i, (name, age)) in enumerate(zip(names, ages))
            ],
        )
        r2 = list_relation(
            ["id", "mark"], [{"id": 4, "mark": 99}, {"id": 6, "mark": 88}]
        )

        result = natural_join(r1, r2)
        expected = list_relation(
            ["id", "name", "age", "mark"],
            [
                {"id": 4, "name": "Martin", "age": 23, "mark": 99},
                {"id": 6, "name": "Standa", "age": 19, "mark": 88},
            ],
        )

        self.assertTrue(compare_relation_members(result, expected))

    def test_division(self):
        subjects = ["math", "math", "math", "math", "english", "english"]
        r1 = list_relation(
            ["name", "subject"],
            [
                {"name": name, "subject": sub}
                for (name, sub) in zip(names[:4] + names[:2], subjects)
            ],
        )
        r2 = list_relation(["subject"], [{"subject": "math"}, {"subject": "english"}])

        result = division(r1, r2)
        expected = list_relation(["name"], [{"name": "Dani"}, {"name": "Emil"}])

        self.assertTrue(compare_relation_members(result, expected))
