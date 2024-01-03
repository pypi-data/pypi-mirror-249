from abc import ABC
from ..relations.relation import Relation


class UnaryOperation(Relation, ABC):
    """Abstract ancestor for any unary operation on a relation

    Attributes
    ----------
    _original_relation : Relation
        unmodified input of the operation
    """

    def __init__(self, relation: Relation):
        """
        Parameters
        ----------
        relation : Relation
            Input of the operation
        """
        super().__init__(relation.get_schema())
        self._original_relation: Relation = relation

    def get_original_relation(self) -> Relation:
        """Gets the unchanged input relation of the operation"""
        return self._original_relation

    def can_be_infinite(self):
        return self.get_original_relation().can_be_infinite()

    def can_is_member_loop(self):
        return self.get_original_relation().can_is_member_loop()
