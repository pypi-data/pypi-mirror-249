from ..relations.relation import Relation
from ..utils.relational_schema import RelationalSchema
from ..utils.conditions import equality_cond
from ..utils.list_operations import is_subset, subtract
from .projection import Projection
from .difference import Difference
from .selection import Selection
from .cross_join import CrossJoin


def intersection(left: Relation, right: Relation) -> Relation:
    """Function representing intersection of two relations

    Parameters
    ----------
    left : Relation
        Left side of the operation
    right : Relation
        Right side of the operation

    Returns
    -------
    Relation
        Relation containing only tuples present in both input relations

    Raises
    ------
    Exception
        If schemas of input relations don't match
    """
    if not left.get_schema() == right.get_schema():
        raise Exception("Cannot intersect relations with different schemas")
    if left.can_be_infinite():
        return Difference(right, Difference(right, left))
    else:
        return Difference(left, Difference(left, right))


def natural_join(left: Relation, right: Relation) -> Relation:
    """Function representing a natural join of two relations

    Parameters
    ----------
    left : Relation
        Left side of the operation
    right : Relation
        Right side of the operation

    Returns
    -------
    Relation
        Relation containing all joined tuples of the input relations
    """
    join_schema, common_attrs = RelationalSchema.join(
        left.get_schema(), right.get_schema()
    )
    result = CrossJoin(left, right)

    for attr in common_attrs:
        result = Selection(result, equality_cond, [attr, attr + "'"])

    return Projection(result, join_schema)


def division(left: Relation, right: Relation) -> Relation:
    """Function representing the division of relations

    Parameters
    ----------
    left : Relation
        Relation to be divided
    right : Relation
        Divisor

    Returns
    -------
    Relation
        A relation that is the result of relational division

    Raises
    ------
    Exception
        If right relation's schema isn't a subset of left one's
    """
    l_schema = left.get_schema()
    r_schema = right.get_schema()
    if not is_subset(r_schema, l_schema):
        raise Exception(
            "Schema of a divisor relation must be a subset of the schema of the relation being divided."
        )

    l_schema_unique = subtract(l_schema, r_schema)
    l_unique = Projection(left, l_schema_unique)

    all_combinations = CrossJoin(l_unique, right)
    missing_combinations = Difference(all_combinations, left)

    return Difference(l_unique, Projection(missing_combinations, l_schema_unique))


def decomposition(r: Relation) -> list:
    """Function that should find functional dependencies in a relation and then split it
    into smaller ones until they all satisfy BCNF

    NOT IMPLEMENTED

    Parameters
    ----------
    r : Relation
        Relation to be decomposed

    Returns
    -------
    list
        A list of relations that all satisfy BCNF and when joined back equal the input relation
    """
    pass
