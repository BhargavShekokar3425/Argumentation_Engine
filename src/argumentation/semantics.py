"""
Computation of Argumentation Semantics:
- Grounded Extension
- Complete Extensions
- Preferred Extensions
- Stable Extensions
- Semi-stable Extensions
"""

from typing import Set, List, Dict, Any
from itertools import combinations
from .framework import ArgumentationFramework
from .defense import (
    is_conflict_free,
    characteristic,
    is_admissible,
    is_complete,
)


def powerset(iterable):
    """Generate all subsets of an iterable, ordered by increasing size."""
    s = list(iterable)
    for r in range(len(s) + 1):
        for combo in combinations(s, r):
            yield set(combo)


def compute_grounded(af: ArgumentationFramework) -> Set[Any]:
    """Compute the unique grounded extension of an argumentation framework.

    The grounded extension is the least fixed point of the characteristic function F,
    computed by iterating from the empty set: S_{k+1} = F(S_k) until S_{k+1} = S_k.

    Args:
        af: The argumentation framework.

    Returns:
        The grounded extension as a set of arguments.
    """
    S: Set[Any] = set()
    while True:
        next_S = characteristic(af, S)
        if next_S == S:
            return S
        S = next_S


def compute_complete(af: ArgumentationFramework) -> List[Set[Any]]:
    """Compute all complete extensions of an argumentation framework.

    A set S is complete iff S is conflict-free and S = F(S).

    Args:
        af: The argumentation framework.

    Returns:
        List of complete extensions (each as a set of arguments).
    """
    complete_exts: List[Set[Any]] = []
    # Exhaustive enumeration over all 2^n subsets
    for candidate in powerset(af.arguments):
        if is_complete(af, candidate):
            complete_exts.append(candidate)
    return complete_exts


def compute_preferred(af: ArgumentationFramework) -> List[Set[Any]]:
    """Compute all preferred extensions of an argumentation framework.

    A preferred extension is an inclusion-maximal admissible set
    (equivalently, an inclusion-maximal complete extension).

    Args:
        af: The argumentation framework.

    Returns:
        List of preferred extensions.
    """
    # Find all admissible sets
    admissible_sets: List[Set[Any]] = [
        candidate for candidate in powerset(af.arguments)
        if is_admissible(af, candidate)
    ]

    preferred: List[Set[Any]] = []
    for S in admissible_sets:
        # Check if S is strictly contained in any other admissible set
        if not any(S < other for other in admissible_sets):
            preferred.append(S)

    return preferred


def compute_stable(af: ArgumentationFramework) -> List[Set[Any]]:
    r"""Compute all stable extensions of an argumentation framework.

    A conflict-free set S is stable iff S attacks every argument outside itself:
    S^+ = A \ S.

    Args:
        af: The argumentation framework.

    Returns:
        List of stable extensions (can be empty if none exist).
    """
    stable_exts: List[Set[Any]] = []
    all_args = af.arguments

    for candidate in powerset(all_args):
        if is_conflict_free(af, candidate):
            attacked = af.attacks_set(candidate)
            outside = all_args - candidate
            if attacked == outside:
                stable_exts.append(candidate)

    return stable_exts


def compute_semi_stable(af: ArgumentationFramework) -> List[Set[Any]]:
    """Compute all semi-stable extensions of an argumentation framework.

    A semi-stable extension is a complete extension whose range (S union S^+)
    is inclusion-maximal among all complete extensions.

    Args:
        af: The argumentation framework.

    Returns:
        List of semi-stable extensions.
    """
    complete_exts = compute_complete(af)
    if not complete_exts:
        return []

    # Map each complete extension to its range: S U S^+
    ranges = [(ext, ext | af.attacks_set(ext)) for ext in complete_exts]

    semi_stable: List[Set[Any]] = []
    for ext, ext_range in ranges:
        # Check if ext_range is strictly contained in any other complete extension's range
        if not any(ext_range < other_range for _, other_range in ranges):
            semi_stable.append(ext)

    return semi_stable


def compute_all_extensions(af: ArgumentationFramework) -> Dict[str, Any]:
    """Compute all extensions for grounded, complete, preferred, stable, and semi-stable semantics.

    Args:
        af: The argumentation framework.

    Returns:
        Dictionary mapping semantic names to their extensions.
    """
    grounded = compute_grounded(af)
    complete = compute_complete(af)

    # Note: Preferred extensions can be directly derived from complete extensions:
    # they are the inclusion-maximal complete extensions.
    preferred = [
        ext for ext in complete
        if not any(ext < other for other in complete)
    ]

    # Stable extensions are complete extensions where S U S^+ == A
    all_args = af.arguments
    stable = [
        ext for ext in complete
        if (ext | af.attacks_set(ext)) == all_args
    ]

    # Semi-stable extensions are complete extensions with inclusion-maximal range
    ranges = [(ext, ext | af.attacks_set(ext)) for ext in complete]
    semi_stable = [
        ext for ext, r in ranges
        if not any(r < other_r for _, other_r in ranges)
    ]

    return {
        "grounded": grounded,
        "complete": complete,
        "preferred": preferred,
        "stable": stable,
        "semi_stable": semi_stable,
    }
