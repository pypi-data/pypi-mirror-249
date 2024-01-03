import unittest
from infinite_relations import *

# CONSTANTS
lr = list_relation(["fib"], [])
lr2 = list_relation(["fib"], [])
ir = fibonacci_relation()
ir2 = fibonacci_relation()


class BooleanFunctionsTest(unittest.TestCase):
    def test_trivial(self):
        self.assertFalse(lr.can_be_infinite())
        self.assertTrue(ir.can_be_infinite())

        self.assertFalse(lr.can_is_member_loop())
        self.assertTrue(ir.can_is_member_loop())

    def test_union(self):
        self.assertFalse(union(lr, lr2).can_be_infinite())
        self.assertTrue(union(lr, ir).can_be_infinite())
        self.assertTrue(union(ir, ir2).can_be_infinite())

        self.assertFalse(union(lr, lr2).can_is_member_loop())
        self.assertTrue(union(lr, ir).can_is_member_loop())
        self.assertTrue(union(ir, ir2).can_is_member_loop())

    def test_difference(self):
        self.assertFalse(difference(lr, lr2).can_be_infinite())
        self.assertFalse(difference(lr, ir).can_be_infinite())
        self.assertTrue(difference(ir, lr).can_be_infinite())
        self.assertTrue(difference(ir, ir2).can_be_infinite())

        self.assertFalse(difference(lr, lr2).can_is_member_loop())
        self.assertTrue(difference(lr, ir).can_is_member_loop())
        self.assertTrue(difference(ir, lr).can_is_member_loop())
        self.assertTrue(difference(ir, ir2).can_is_member_loop())

    def test_cross_join(self):
        self.assertFalse(cross_join(lr, lr2).can_be_infinite())
        self.assertTrue(cross_join(lr, ir).can_be_infinite())
        self.assertTrue(cross_join(ir, lr).can_be_infinite())
        self.assertTrue(cross_join(ir, ir2).can_be_infinite())

        self.assertFalse(cross_join(lr, lr2).can_is_member_loop())
        self.assertTrue(cross_join(lr, ir).can_is_member_loop())
        self.assertTrue(cross_join(ir, lr).can_is_member_loop())
        self.assertTrue(cross_join(ir, ir2).can_is_member_loop())

    def test_projection(self):
        self.assertFalse(projection(lr, ["fib"]).can_be_infinite())
        self.assertTrue(projection(ir, ["fib"]).can_be_infinite())

        self.assertFalse(projection(lr, ["fib"]).can_is_member_loop())
        self.assertTrue(projection(ir, ["fib"]).can_is_member_loop())

    def test_selection(self):
        self.assertFalse(selection(lr, empty_cond).can_be_infinite())
        self.assertTrue(selection(ir, empty_cond).can_be_infinite())

        self.assertFalse(selection(lr, empty_cond).can_is_member_loop())
        self.assertTrue(selection(ir, empty_cond).can_is_member_loop())

    def test_intersection(self):
        self.assertFalse(intersection(lr, lr2).can_be_infinite())
        self.assertFalse(intersection(lr, ir).can_be_infinite())
        self.assertTrue(intersection(ir, ir2).can_be_infinite())

        self.assertFalse(intersection(lr, lr2).can_is_member_loop())
        self.assertTrue(intersection(lr, ir).can_is_member_loop())
        self.assertTrue(intersection(ir, ir2).can_is_member_loop())

    def test_natural_join(self):
        self.assertFalse(natural_join(lr, lr2).can_be_infinite())
        self.assertTrue(natural_join(lr, ir).can_be_infinite())
        self.assertTrue(natural_join(ir, lr).can_be_infinite())
        self.assertTrue(natural_join(ir, ir2).can_be_infinite())

        self.assertFalse(natural_join(lr, lr2).can_is_member_loop())
        self.assertTrue(natural_join(lr, ir).can_is_member_loop())
        self.assertTrue(natural_join(ir, lr).can_is_member_loop())
        self.assertTrue(natural_join(ir, ir2).can_is_member_loop())

    def test_division(self):
        self.assertFalse(division(lr, lr2).can_be_infinite())
        self.assertFalse(division(lr, ir).can_be_infinite())
        self.assertTrue(division(ir, lr).can_be_infinite())
        self.assertTrue(division(ir, ir2).can_be_infinite())

        self.assertFalse(division(lr, lr2).can_is_member_loop())
        self.assertTrue(division(lr, ir).can_is_member_loop())
        self.assertTrue(division(ir, lr).can_is_member_loop())
        self.assertTrue(division(ir, ir2).can_is_member_loop())
