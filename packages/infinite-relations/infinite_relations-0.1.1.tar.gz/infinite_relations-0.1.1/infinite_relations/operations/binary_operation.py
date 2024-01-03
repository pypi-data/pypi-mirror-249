from __future__ import annotations
from abc import ABC
from ..relations.relation import Relation


# předek pro binární operace relační algebry, abstraktní třída
class BinaryOperation(Relation, ABC):
    """Abstract ancestor for all binary operations on relations

    Attributes
    ----------
    left : Relation
        Left side of the operation, unmodified
    right : Relation
        Right side of the operation, unmodified
    """

    def __init__(self, schema: list, left: Relation, right: Relation):
        """
        Parameters
        ----------
        schema : list
            Schema of the resulting relation
        left : Relation
            Left side of the operation
        right : Relation
            Right side of the operation
        """
        super().__init__(schema)
        self._left = left
        self._right = right

    def get_left(self) -> Relation:
        """Gets original relation from the left side of the operation"""
        return self._left

    def get_right(self) -> Relation:
        """Gets original relation from the right side of the operation"""
        return self._right
