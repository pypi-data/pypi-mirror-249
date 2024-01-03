from ..relations.relation import Relation
from .binary_operation import BinaryOperation


class Difference(BinaryOperation):
    """Difference between two relations"""

    def __init__(self, left: Relation, right: Relation):
        """Subtracts right relation from left

        Not commutative

        Parameters
        ----------
        left : Relation
            Left side of the operation
        right : Relation
            Right side of the operation

        Raises
        ------
        Exception
            If left and right have different schemas
        """
        if not left.get_schema() == right.get_schema():
            raise Exception("Cannot subtract relations with different schemas")
        super().__init__(left.get_schema(), left, right)

    def can_be_infinite(self):
        return self.get_left().can_be_infinite()

    def can_is_member_loop(self):
        return (
            self.get_left().can_is_member_loop()
            or self.get_right().can_is_member_loop()
        )

    def is_member(self, element):
        return self.get_left().is_member(element) and not self.get_right().is_member(
            element
        )

    def members(self):
        """Yields all tuples of left relation that are absent in the right"""
        return (
            tpl
            for tpl in self.get_left().members()
            if not self.get_right().is_member(tpl)
        )
