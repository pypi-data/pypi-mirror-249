from __future__ import annotations
from .relation import Relation


class ListRelation(Relation):
    """Relation with a finite number of members, initiated by a list

    Attributes
    ----------
    _schema : list
        A list of attributes
    _members : list
        A list of contained tuples
    """

    def __init__(self, schema: list, tuples: list = []):
        """Creates a finite relation from a given schema and a list of tuples

        Parameters
        ----------
        schema : list
            A list of attribute names
        tuples : list, optional
            A list of tuples (dicts) to initialize the relation, by default []

        Raises
        ------
        Exception
            If length of schema and a tuple don't match
        TypeError
            If a tuple is not a dict
        """
        for tuple in tuples:
            if len(schema) != len(tuple):
                raise Exception("Length of schema and tuples must match")
            if not isinstance(tuple, dict):
                raise TypeError("Tuples must be dictionaries")
        super().__init__(schema)
        self._members = tuples

    def can_be_infinite(self):
        return False

    def can_is_member_loop(self):
        return False

    def members(self):
        """Returns an iterator from a finite member list"""
        return iter(self._members)
