from .binary_operation import BinaryOperation
from ..utils.relational_schema import RelationalSchema
from ..relations.relation import Relation
from ..utils.list_operations import dict_from_lists, dict_values
from itertools import islice


class CrossJoin(BinaryOperation):
    """Cross join (Cartesian product) of two relations"""

    def __init__(self, left: Relation, right: Relation):
        """Multiplies left relation with right

        Not commutative

        Parameters
        ----------
        left : Relation
            Left side of the operation
        right : Relation
            Right side of the operation
        """
        super().__init__(
            RelationalSchema.cross(left.get_schema(), right.get_schema()),
            left,
            right,
        )

    def can_be_infinite(self):
        return self.get_left().can_be_infinite() or self.get_right().can_be_infinite()

    def can_is_member_loop(self):
        return (
            self.get_left().can_is_member_loop()
            or self.get_right().can_is_member_loop()
        )

    def is_member(self, tpl: dict) -> bool:
        l_tuple, r_tuple = self._split_tuple(tpl)
        return self.get_left().is_member(l_tuple) and self.get_right().is_member(
            r_tuple
        )

    def members(self):
        """Combines every tuple from the left relation with every tuple from the right"""
        if not self.get_left().can_be_infinite():
            for r_tuple in self.get_right().members():
                for l_tuple in self.get_left().members():
                    yield self._cross_tuple(l_tuple, r_tuple)
        elif not self.get_right().can_be_infinite():
            for l_tuple in self.get_left().members():
                for r_tuple in self.get_right().members():
                    yield self._cross_tuple(l_tuple, r_tuple)
        else:
            limit = 0
            while True:
                for i in range(limit + 1):
                    l = next(islice(self.get_left().members(), i, None))
                    r = next(islice(self.get_right().members(), limit - i, None))
                    yield self._cross_tuple(l, r)
                limit += 1

    def _cross_tuple(self, l_tuple: dict, r_tuple: dict) -> dict:
        """Helper function to combine two tuples

        Parameters
        ----------
        l_tuple : dict
            Tuple from the left side of the cross operation
        r_tuple : dict
            Tuple from the right side of the cross operation

        Returns
        -------
        dict
            A tuple with a new schema and both tuple's combined values
        """
        return dict_from_lists(
            self.get_schema(),
            list(l_tuple.values()) + list(r_tuple.values()),
        )

    def _split_tuple(self, tuple: dict) -> tuple[dict, dict]:
        """Helper function to split a combined tuple into it's original ones

        Parameters
        ----------
        tuple : dict
            Combined/crossed tuple to be split

        Returns
        -------
        tuple[dict, dict]
            A tuple of two relational tuples from the original relations
        """
        l_schema = self.get_left().get_schema()
        r_schema = self.get_right().get_schema()
        s_schema = self.get_schema()

        cross_l_schema = [attr if attr in s_schema else attr + "'" for attr in l_schema]
        cross_r_schema = [attr if attr in s_schema else attr + "'" for attr in r_schema]

        l_tuple = dict_from_lists(l_schema, dict_values(tuple, cross_l_schema))
        r_tuple = dict_from_lists(r_schema, dict_values(tuple, cross_r_schema))

        return (l_tuple, r_tuple)
