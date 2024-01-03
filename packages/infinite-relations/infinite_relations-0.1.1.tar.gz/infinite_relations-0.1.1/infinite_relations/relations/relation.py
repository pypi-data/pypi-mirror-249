from __future__ import annotations
from abc import ABC, abstractclassmethod
from ..utils.relational_schema import RelationalSchema
from ..utils.list_operations import compare_lists_orderless
from typing import Iterable


class Relation(ABC):
    """Abstract ancestor containing attributes and methods common to all relations

    Attributes
    ----------
    _schema : list
        A list of attribute names
    """

    def __init__(self, schema: list):
        """
        Parameters
        ----------
        schema : list
            A list of attribute names
        """
        self._schema: list = schema

    def get_schema(self) -> list:
        """Gets relation's schema"""
        return self._schema

    def rename(self, old_names: list, new_names: list) -> Relation:
        """Helper function to rename relation's attributes without having to create a new one

        Parameters
        ----------
        relation : Relation
            Relation to rename attributes of
        old_names : list
            List of attribute names to be changed
        new_names : list
            New attribute names

        Returns
        -------
        Relation
            Relation with a new schema
        """
        new_attrs = []
        for attr in self.get_schema():
            if attr in old_names:
                new_name = new_names[old_names.index(attr)]
                new_unique_name = RelationalSchema.get_unique_attr_name(
                    new_name, new_attrs
                )
                new_attrs.append(new_unique_name)
            else:
                new_attrs.append(attr)
        self._schema = new_attrs

    def can_be_infinite(self) -> bool:
        """
        Returns
        -------
        bool
            True, if the relation can contain an infinite number of tuples
        """
        return True

    def can_is_member_loop(self) -> bool:
        """
        Returns
        -------
        bool
            True, if is_member() can get stuck in an infinite loop without giving an answer
        """
        return True

    @abstractclassmethod
    def members(self) -> Iterable:
        """Iterable containing relation's tuples

        Every derived class must implement it's own members() method

        Returns
        -------
        Iterable
            Iterable containing relation's tuples
        """
        pass

    def list_members(self, count: int = -1) -> list:
        """Gets a given number of tuples in a list

        Good for use with infinite relations where you can't get all the members

        Parameters
        ----------
        count : int
            Number of tuples to extract, by default -1
            If not supplied, will yield all members of a list relation or first 10 members of an infinite relation

        Returns
        -------
        list
            List of first x member tuples
        """
        members = self.members()

        if count == -1:
            if not self.can_be_infinite():
                return list(members)
            else:
                count = 10

        member_list = []
        for _ in range(count):
            member_list.append(next(members))
        return member_list

    def can_be_member(self, tpl: dict) -> bool:
        """Checks if a tuple is of the right type

        Parameters
        ----------
        tpl : dict
            Tuple to check

        Returns
        -------
        bool
            True, if tpl is of the right type
        """
        return compare_lists_orderless(self.get_schema(), list(tpl.keys()))

    def is_member(self, tpl: dict) -> bool:
        """Checks if a tuple is contained in the relation

        Can potentially get stuck in an infinite loop without giving an answer.
        Check can_is_member_loop()

        Parameters
        ----------
        tpl : dict
            Tuple to check if it's contained in the relation

        Returns
        -------
        bool
            True, if tpl is contained in the relation
        """
        if not self.can_be_member(tpl):
            return False
        return tpl in self.members()

    def print(self, limit: int = 10_000) -> None:
        """Prints the schema then iterates over member tuples and prints their values in rows

        Parameters
        ----------
        limit : int
            Maximum number of printed members, useful for printing infinite relations
        """
        print("============")
        RelationalSchema.print(self.get_schema())
        print("------------")
        for tpl in self.members():
            print(*tpl.values())
            limit -= 1
            if limit == 0:
                break
        print("============")

    def _distinct(self, members: Iterable) -> Iterable:
        """Stores yielded tuples to avoid yielding duplicates

        Parameters
        ----------
        members: Iterable
            Iterable with potentially duplicate tuples

        Returns
        -------
        Iterable
            Iterable with no duplicates
        """
        yielded = []
        for item in members():
            if not item in yielded:
                yielded.append(item)
                yield item
