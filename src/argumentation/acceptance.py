"""
Argument Acceptance Status module.

Computes whether a given argument alpha is:
- Skeptically accepted: alpha in all extensions of the semantics (intersection).
- Credulously accepted: alpha in at least one extension of the semantics (union).
- Rejected / Not accepted: alpha in no extension of the semantics.
"""

from typing import Set, List, Dict, Any, Union, Optional
from .framework import ArgumentationFramework
from .semantics import (
    compute_grounded,
    compute_complete,
    compute_preferred,
    compute_stable,
    compute_semi_stable,
    compute_all_extensions,
)


def get_extensions_for_semantics(
    af: ArgumentationFramework, semantics: str
) -> List[Set[Any]]:
    """Get the list of extensions for a specified semantics.

    Supported semantics:
    'grounded', 'complete', 'preferred', 'stable', 'semi_stable'
    """
    sem = semantics.lower().replace("-", "_").strip()
    if sem == "grounded":
        return [compute_grounded(af)]
    elif sem == "complete":
        return compute_complete(af)
    elif sem == "preferred":
        return compute_preferred(af)
    elif sem == "stable":
        return compute_stable(af)
    elif sem in ("semi_stable", "semistable"):
        return compute_semi_stable(af)
    else:
        raise ValueError(
            f"Unknown semantics '{semantics}'. Supported: grounded, complete, preferred, stable, semi_stable."
        )


def argument_acceptance_status(
    af: ArgumentationFramework,
    argument: Any,
    semantics: str = "preferred",
    extensions: Optional[List[Set[Any]]] = None,
) -> Dict[str, Any]:
    """Report the acceptance status of argument alpha under the specified semantics.

    Args:
        af: The argumentation framework.
        argument: The argument alpha to evaluate.
        semantics: The chosen semantics ('grounded', 'complete', 'preferred', 'stable', 'semi_stable').
        extensions: Precomputed extensions for this semantics (optional).

    Returns:
        Dictionary with:
            - argument: alpha
            - semantics: name of semantics
            - status: 'skeptical', 'credulous_only', or 'rejected'
            - is_skeptical: bool
            - is_credulous: bool
            - num_extensions: count of extensions
            - extensions: list of extensions
    """
    if argument not in af.arguments:
        return {
            "argument": argument,
            "semantics": semantics,
            "status": "rejected",
            "is_skeptical": False,
            "is_credulous": False,
            "num_extensions": 0,
            "extensions": [],
            "reason": f"Argument '{argument}' not in framework arguments.",
        }

    if extensions is None:
        extensions = get_extensions_for_semantics(af, semantics)

    num_exts = len(extensions)

    # Edge case: No extensions exist (e.g. Stable semantics on odd cycle)
    if num_exts == 0:
        return {
            "argument": argument,
            "semantics": semantics,
            "status": "rejected",
            "is_skeptical": False,
            "is_credulous": False,
            "num_extensions": 0,
            "extensions": [],
            "reason": f"No {semantics} extensions exist for this framework.",
        }

    # Credulous acceptance: in at least one extension
    is_credulous = any(argument in ext for ext in extensions)

    # Skeptical acceptance: in every extension
    is_skeptical = all(argument in ext for ext in extensions)

    if is_skeptical:
        status = "skeptical"
    elif is_credulous:
        status = "credulous_only"
    else:
        status = "rejected"

    return {
        "argument": argument,
        "semantics": semantics,
        "status": status,
        "is_skeptical": is_skeptical,
        "is_credulous": is_credulous,
        "num_extensions": num_exts,
        "extensions": [sorted(list(ext), key=lambda x: str(x)) for ext in extensions],
    }
