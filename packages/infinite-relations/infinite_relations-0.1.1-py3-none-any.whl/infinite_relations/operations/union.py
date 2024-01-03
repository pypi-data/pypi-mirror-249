from itertools import zip_longest
from ..relations.relation import Relation
from .binary_operation import BinaryOperation
from ..utils.list_operations import flatten_list


class Union(BinaryOperation):
    """Union of two relations"""

    def __init__(self, left: Relation, right: Relation):
        """Unites left relation with right

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
            raise Exception("Cannot unite relations with different schemas")
        super().__init__(left.get_schema(), left, right)

    def can_be_infinite(self):
        return self.get_left().can_be_infinite() or self.get_right().can_be_infinite()

    def can_is_member_loop(self):
        return (
            self.get_left().can_is_member_loop()
            or self.get_right().can_is_member_loop()
        )

    def is_member(self, element):
        if self.get_left().can_is_member_loop():
            return self.get_right().is_member(element) or self.get_left().is_member(
                element
            )
        else:
            return self.get_left().is_member(element) or self.get_right().is_member(
                element
            )

    def members(self):
        """Yields tuples from left and right relations alternately"""
        return self._distinct(self._members)

    def _members(self):
        """Helper generator function that zips together tuples of both relations

        Doesn't handle duplicates
        """
        for item in zip_longest(self.get_left().members(), self.get_right().members()):
            if not item[0] == None:
                yield item[0]
            if not item[1] == None:
                yield item[1]
