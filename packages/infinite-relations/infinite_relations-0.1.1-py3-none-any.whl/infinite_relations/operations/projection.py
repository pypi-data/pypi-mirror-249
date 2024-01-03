from __future__ import annotations

from ..relations.relation import Relation
from ..utils.list_operations import is_subset
from .unary_operation import UnaryOperation


class Projection(UnaryOperation):
    """Relation projected onto a new schema"""

    def __init__(self, relation: Relation, new_schema: list):
        """Projects relation onto new schema

        Parameters
        ----------
        relation : Relation
            Input relation of the operation
        new_schema : list
            New schema to project the relation onto

        Raises
        ------
            Exception
                If new schema isn't a subset of the relation's current schema
        """
        if is_subset(new_schema, relation.get_schema()):
            super().__init__(relation)
            self._new_schema = new_schema
        else:
            raise Exception("Schema of projection must be a subset of original schema")

    def can_is_member_loop(self):
        return self.can_be_infinite()

    def members(self):
        """Yields all tuples of the original relation projected on the new schema"""
        return self._distinct(self._members)

    def _members(self):
        """Helper generator function that yields projected tuples

        Doesn't handle duplicates
        """
        for tpl in self.get_original_relation().members():
            yield {attr: tpl[attr] for attr in self.get_schema()}

    def get_schema(self):
        return self._new_schema
