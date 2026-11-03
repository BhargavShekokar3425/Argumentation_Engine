"""
Fundamental argumentation concepts: conflict-freeness, defense,
the characteristic function, admissibility, and completeness.
"""

from typing import Set, Any
from .framework import ArgumentationFramework


def is_conflict_free(af: ArgumentationFramework, argument_set: Set[Any]) -> bool:
    """Check whether a set S of arguments is conflict-free in framework af.

    A set S is conflict-free iff there are no arguments a, b in S such that (a, b) in R.

    Args:
        af: The argumentation framework.
        argument_set: Set S of arguments to check.

    Returns:
        True if S is conflict-free, False otherwise.
    """
    S = set(argument_set)
    for a in S:
        if af.targets[a] & S:
            return False
    return True


def defends(af: ArgumentationFramework, argument_set: Set[Any], argument: Any) -> bool:
    """Determine whether set S defends argument alpha.

    Set S defends argument alpha iff for every b in A such that (b, alpha) in R,
    there exists c in S such that (c, b) in R (i.e. all attackers of alpha are
    counterattacked by S).

    Args:
        af: The argumentation framework.
        argument_set: Defending set S.
        argument: The candidate argument alpha.

    Returns:
        True if S defends alpha, False otherwise.
    """
    if argument not in af.arguments:
        return False

    attackers_of_arg = af.attackers[argument]
    if not attackers_of_arg:
        # Arguments with no attackers are defended by every set (including the empty set)
        return True

    # Compute all targets of S: S^+
    s_attacked = af.attacks_set(argument_set)

    # S defends alpha iff every attacker of alpha is in S^+
    return attackers_of_arg.issubset(s_attacked)


def characteristic(af: ArgumentationFramework, argument_set: Set[Any]) -> Set[Any]:
    """Characteristic function F_AF(S).

    Returns the set of all arguments in A that are defended by set S.

    Args:
        af: The argumentation framework.
        argument_set: Defending set S.

    Returns:
        Set of arguments defended by S.
    """
    return {a for a in af.arguments if defends(af, argument_set, a)}


def is_admissible(af: ArgumentationFramework, argument_set: Set[Any]) -> bool:
    """Check whether set S is admissible in framework af.

    A set S is admissible iff S is conflict-free and S defends all its members
    (i.e. S subseteq F(S)).

    Args:
        af: The argumentation framework.
        argument_set: Set S to check.

    Returns:
        True if S is admissible, False otherwise.
    """
    S = set(argument_set)
    if not is_conflict_free(af, S):
        return False
    return S.issubset(characteristic(af, S))


def is_complete(af: ArgumentationFramework, argument_set: Set[Any]) -> bool:
    """Check whether set S is a complete extension in framework af.

    A set S is a complete extension iff S is conflict-free and S = F(S)
    (i.e. S is a conflict-free fixed point of the characteristic function).

    Args:
        af: The argumentation framework.
        argument_set: Set S to check.

    Returns:
        True if S is a complete extension, False otherwise.
    """
    S = set(argument_set)
    if not is_conflict_free(af, S):
        return False
    return S == characteristic(af, S)
