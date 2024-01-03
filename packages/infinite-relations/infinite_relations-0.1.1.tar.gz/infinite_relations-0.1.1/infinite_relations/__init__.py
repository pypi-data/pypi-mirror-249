"""This module contains tools for creating and operating on both finite and infinite relations

Constructor Functions
---------------------
    list_relation(schema)
    integer_relation(schema)
    general_integer_relation(schema, condition)
    add_relation(schema)

Basic Operations
----------------
    union(left, right)
    difference(left, right)
    cross_join(left, right)
    projection(relation, new_schema)
    selection(relation, condition, condition_params)

Derived Operations
------------------
    intersection(left, right)
    natural_join(left, right)
    division(left, right)
"""
from .relations.relation import Relation
from .relations.list_relation import ListRelation
from .relations.infinite_relations import (
    GeneralIntegerRelation,
    AddRelation,
    IntegerRelation,
    FibonacciRelation,
    EqualRelation,
    UnequalRelation,
    WordRelation,
)
from .operations.union import Union
from .operations.difference import Difference
from .operations.cross_join import CrossJoin
from .operations.projection import Projection
from .operations.selection import Selection
from .operations.derived import *
from .utils.conditions import *
from .utils.list_operations import *


# basic constructor functions
def list_relation(schema: list, tuples: list) -> ListRelation:
    """Creates a finite relation from a list of attribute names and a list of tuples

    Parameters
    ----------
    schema : list
        List of attribute names
    tuples : list, optional
        A list of tuples to initialize the relation, by default []

    Returns
    -------
    ListRelation
        New finite relation
    """
    return ListRelation(schema, tuples)


def integer_relation(schema: list = ["n"]) -> IntegerRelation:
    """Creates unary integer relation with a given one-attribute schema

    Parameters
    ----------
    schema : list, optional
        List of attribute names, by default ["n"]

    Returns
    -------
    IntegerRelation
        New unary relation of non-negative integers
    """
    return IntegerRelation(schema)


def general_integer_relation(
    schema: list, condition: callable
) -> GeneralIntegerRelation:
    """Creates an infinite relation of integer tuples determined by a given schema and condition

    Parameters
    ----------
    schema : list
        List of attribute names
    condition : callable
        Condition that tuples must satisfy (i.e. lambda x: x % 2 == 0)

    Returns
    -------
    GeneralIntegerRelation
        New infinite relation of integer tuples, determined by the condition
    """
    return GeneralIntegerRelation(schema, condition)


# premade infinite relations
def add_relation(schema: list = ["x", "y", "sum"]) -> AddRelation:
    """Creates an add relation with a given schema

    Parameters
    ----------
    schema : list, optional
        List of attribute names, by default ["x", "y", "sum"]

    Returns
    -------
    AddRelation
        New infinite relation of all possible integer sums
    """
    return AddRelation(schema)


def fibonacci_relation() -> FibonacciRelation:
    return FibonacciRelation()


def equal_relation(schema: list = ["x", "y"]) -> EqualRelation:
    return EqualRelation(schema)


def unequal_relation() -> UnequalRelation:
    return UnequalRelation()


def word_relation(schema: list = ["word"]) -> WordRelation:
    return WordRelation(schema)


# basic operations
def union(left: Relation, right: Relation) -> Union:
    """Unites left relation with right

    Parameters
    ----------
    left : Relation
        Left side of the operation
    right : Relation
        Right side of the operation

    Returns
    -------
    Union
        New united relation
    """
    return Union(left, right)


def difference(left: Relation, right: Relation) -> Difference:
    """Subtracts right relation from left

    Not commutative

    Parameters
    ----------
    left : Relation
        Left side of the operation
    right : Relation
        Right side of the operation

    Returns
    -------
    Difference
        New differential relation
    """
    return Difference(left, right)


def cross_join(left: Relation, right: Relation) -> CrossJoin:
    """Multiplies left relation with right

    Not commutative

    Parameters
    ----------
    left : Relation
        Left side of the operation
    right : Relation
        Right side of the operation

    Returns
    -------
    CrossJoin
        New Cartesian product of relations
    """
    return CrossJoin(left, right)


def projection(relation: Relation, new_schema: list) -> Projection:
    """Projects relation onto new schema

    Parameters
    ----------
    relation : Relation
        Input relation of the operation
    new_schema : list
        New schema to project the relation onto

    Returns
    -------
    Projection
        New projected relation
    """
    return Projection(relation, new_schema)


def selection(
    left: Relation, condition: callable, condition_param_names: list = []
) -> Selection:
    """Restricts the relation to tuples that satisfy a condition

    Parameters
    ----------
    relation : Relation
        Input relation of the operation
    condition : function
        Condition, that tuples must satisfy
    condition_param_names : list
        List of attribute names to be evaluated by the condition

    Returns
    -------
    Selection
        New restricted relation
    """
    return Selection(left, condition, condition_param_names)


# derived operations are already exported in the correct format
