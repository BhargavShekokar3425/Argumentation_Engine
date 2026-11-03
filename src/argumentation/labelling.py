"""
Argumentation Labellings (IN / OUT / UNDEC).

Implements Caminada's 3-valued argumentation labellings:
- IN: Argument is accepted.
- OUT: Argument is rejected (defeated by an accepted argument).
- UNDEC: Argument is undecided.
"""

from typing import Set, Dict, List, Any, Optional
from .framework import ArgumentationFramework
from .semantics import compute_complete


class Labelling:
    """Represents a 3-valued argument labelling."""

    def __init__(self, in_set: Set[Any], out_set: Set[Any], undec_set: Set[Any]) -> None:
        self.in_set: Set[Any] = set(in_set)
        self.out_set: Set[Any] = set(out_set)
        self.undec_set: Set[Any] = set(undec_set)

    def to_dict(self) -> Dict[str, List[Any]]:
        return {
            "IN": sorted(list(self.in_set), key=lambda x: str(x)),
            "OUT": sorted(list(self.out_set), key=lambda x: str(x)),
            "UNDEC": sorted(list(self.undec_set), key=lambda x: str(x)),
        }

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Labelling):
            return False
        return (
            self.in_set == other.in_set
            and self.out_set == other.out_set
            and self.undec_set == other.undec_set
        )

    def __hash__(self) -> int:
        return hash((frozenset(self.in_set), frozenset(self.out_set), frozenset(self.undec_set)))

    def __repr__(self) -> str:
        in_s = sorted(list(self.in_set), key=lambda x: str(x))
        out_s = sorted(list(self.out_set), key=lambda x: str(x))
        und_s = sorted(list(self.undec_set), key=lambda x: str(x))
        return f"Labelling(IN={in_s}, OUT={out_s}, UNDEC={und_s})"


def is_legal_labelling(af: ArgumentationFramework, labelling: Labelling) -> bool:
    """Verify whether a labelling satisfies Caminada's legal labelling conditions:
    1. IN iff every attacker is OUT.
    2. OUT iff at least one attacker is IN.
    3. UNDEC iff no attacker is IN and at least one attacker is UNDEC.

    Args:
        af: The argumentation framework.
        labelling: The candidate labelling.

    Returns:
        True if legal, False otherwise.
    """
    all_args = af.arguments
    if labelling.in_set | labelling.out_set | labelling.undec_set != all_args:
        return False
    if labelling.in_set & labelling.out_set or labelling.in_set & labelling.undec_set or labelling.out_set & labelling.undec_set:
        return False

    for x in af.arguments:
        attackers = af.attackers[x]
        if x in labelling.in_set:
            # Condition 1: Every attacker must be OUT
            if not all(y in labelling.out_set for y in attackers):
                return False
        elif x in labelling.out_set:
            # Condition 2: At least one attacker must be IN
            if not any(y in labelling.in_set for y in attackers):
                return False
        elif x in labelling.undec_set:
            # Condition 3: No attacker is IN and at least one attacker is UNDEC
            if any(y in labelling.in_set for y in attackers):
                return False
            if not any(y in labelling.undec_set for y in attackers):
                return False
        else:
            return False

    return True


def labelling_from_complete_extension(
    af: ArgumentationFramework, complete_ext: Set[Any]
) -> Labelling:
    r"""Derive a legal labelling from a complete extension E:
    IN = E
    OUT = E^+
    UNDEC = A \ (IN U OUT)
    """
    in_set = set(complete_ext)
    out_set = af.attacks_set(in_set)
    undec_set = af.arguments - (in_set | out_set)
    return Labelling(in_set=in_set, out_set=out_set, undec_set=undec_set)


def compute_legal_labellings(
    af: ArgumentationFramework, complete_extensions: Optional[List[Set[Any]]] = None
) -> List[Labelling]:
    """Generate all legal (IN / OUT / UNDEC) labellings for an argumentation framework.

    By Caminada's Theorem, there is a bijective correspondence between complete
    extensions and legal labellings.

    Args:
        af: The argumentation framework.
        complete_extensions: Precomputed complete extensions (optional).

    Returns:
        List of legal Labelling objects.
    """
    if complete_extensions is None:
        complete_extensions = compute_complete(af)

    labellings = [
        labelling_from_complete_extension(af, ext)
        for ext in complete_extensions
    ]
    return labellings
