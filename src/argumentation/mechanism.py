"""
Strategic Argumentation Mechanism Module.

Implements the Grounded Direct Argumentation Mechanism, agent utilities,
and best response computation.
"""

from typing import Set, Dict, List, Any, Tuple, Optional
from itertools import combinations
from .framework import ArgumentationFramework
from .semantics import compute_grounded, powerset


def grounded_direct_mechanism(
    global_af: ArgumentationFramework,
    reports: Dict[Any, Set[Any]]
) -> Set[Any]:
    """Execute the Grounded Direct Argumentation Mechanism.

    Given the global argumentation framework and the subsets revealed by each agent,
    construct the induced framework on the union of revealed arguments and compute
    its grounded extension.

    Args:
        global_af: The complete argumentation framework.
        reports: Mapping from agent identifier to their revealed subset of arguments.

    Returns:
        The grounded extension of the induced framework.
    """
    if not reports:
        return set()

    revealed: Set[Any] = set().union(*reports.values())
    induced_af = global_af.induced_subgraph(revealed)
    return compute_grounded(induced_af)


def agent_utility(
    owned_arguments: Set[Any],
    grounded_outcome: Set[Any]
) -> int:
    """Compute an agent's utility: u_i = |A_i intersect g(R)|.

    The utility is the number of the agent's ACTUAL owned arguments accepted
    in the grounded extension of the revealed graph.

    Args:
        owned_arguments: True set of arguments owned by the agent (A_i).
        grounded_outcome: The grounded extension outcome g(R).

    Returns:
        Integer utility value.
    """
    return len(owned_arguments & grounded_outcome)


def compute_best_responses(
    global_af: ArgumentationFramework,
    agent_id: Any,
    partition: Dict[Any, Set[Any]],
    other_reports: Dict[Any, Set[Any]],
    cache: Optional[Dict[frozenset, Set[Any]]] = None
) -> Tuple[int, List[Set[Any]], int, bool]:
    """Enumerate every subset of A_i that agent i could reveal, given fixed reports
    by the other agents, and return the reports that maximize agent i's utility.

    Args:
        global_af: The global argumentation framework.
        agent_id: Identifier of the agent choosing a report.
        partition: Full agent partition {agent_id: owned_arguments}.
        other_reports: Fixed reports of other agents {other_id: revealed_set}.
        cache: Optional precomputed cache mapping frozenset(revealed_args) -> grounded_ext.

    Returns:
        Tuple of:
            - max_utility: Maximum achievable utility.
            - best_reports: List of all subsets S_i subseteq A_i achieving max_utility.
            - truthful_utility: Utility achieved by reporting A_i truthfully.
            - is_truthful_optimal: True if truthful report achieves max_utility.
    """
    A_i = partition[agent_id]
    other_revealed = set().union(*other_reports.values()) if other_reports else set()

    max_util = -1
    best_reports: List[Set[Any]] = []
    truthful_util = -1

    # Candidate reports: all subsets of A_i
    for report in powerset(A_i):
        revealed_total = other_revealed | report
        rev_key = frozenset(revealed_total)

        if cache is not None and rev_key in cache:
            outcome = cache[rev_key]
        else:
            induced_af = global_af.induced_subgraph(revealed_total)
            outcome = compute_grounded(induced_af)
            if cache is not None:
                cache[rev_key] = outcome

        u = agent_utility(A_i, outcome)

        if report == A_i:
            truthful_util = u

        if u > max_util:
            max_util = u
            best_reports = [report]
        elif u == max_util:
            best_reports.append(report)

    is_truthful_optimal = (truthful_util == max_util)
    return max_util, best_reports, truthful_util, is_truthful_optimal
