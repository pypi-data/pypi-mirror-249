from __future__ import annotations

from ..utils.list_operations import dict_values
from ..relations.relation import Relation
from .unary_operation import UnaryOperation
from inspect import getfullargspec


class Selection(UnaryOperation):
    """Class representing a selection (restriction) of a relation"""

    def __init__(
        self, relation: Relation, condition: function, condition_param_names: list
    ):
        """Restricts the relation to tuples that satisfy a condition

        Parameters
        ----------
        relation : Relation
            Input relation of the operation
        condition : function
            Condition, that tuples must satisfy
        condition_param_names : list
            List of attribute names to be evaluated by the condition

        Raises
        ------
        Exception
            If number of condition parameters isn't empty and doesn't match the condition
        """
        arglen = len(getfullargspec(condition).args)
        if arglen == 0 or arglen == len(condition_param_names):
            self.condition_param_names = condition_param_names
        elif arglen == len(relation.get_schema()):
            self.condition_param_names = relation.get_schema()
        else:
            raise Exception(
                "Number of parameters in condition must either a) be 0; b) match condition_param_names length; c) match relation schema length."
            )
        super().__init__(relation)
        self.condition = condition

    def is_member(self, tpl):
        return self.get_original_relation().is_member(tpl) and self.condition(
            *dict_values(tpl, self.condition_param_names)
        )

    def members(self):
        """Yields tuples from the original relation if they satisfy the condition"""
        for tpl in self.get_original_relation().members():
            condition_params = dict_values(tpl, self.condition_param_names)
            if self.condition(*condition_params):
                yield tpl
