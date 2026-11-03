"""
Strategyproofness Verification Module (Theorems 5.3 and 5.4).

- Theorem 5.3: Exact strategyproofness check via exhaustive best-response verification.
- Theorem 5.4: Structural condition check via odd-length attack path / walk detection.
"""

from typing import Set, Dict, List, Any, Tuple, Optional
from collections import deque
from itertools import product
from .framework import ArgumentationFramework
from .semantics import compute_grounded, powerset
from .mechanism import agent_utility


def precompute_grounded_cache(
    global_af: ArgumentationFramework
) -> Dict[frozenset, Set[Any]]:
    """Precompute the grounded extension for every subset of arguments.

    For n <= 8, 2^n <= 256, so precomputing all subgraphs is extremely fast
    and avoids recomputing identical outcomes during strategyproofness checks.
    """
    cache: Dict[frozenset, Set[Any]] = {}
    for subset in powerset(global_af.arguments):
        fs = frozenset(subset)
        sub_af = global_af.induced_subgraph(subset)
        cache[fs] = compute_grounded(sub_af)
    return cache


def check_theorem_5_3(
    global_af: ArgumentationFramework,
    partition: Dict[Any, Set[Any]],
    cache: Optional[Dict[frozenset, Set[Any]]] = None
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """Verify Theorem 5.3: Exact Strategyproofness.

    A mechanism is strategyproof iff for every agent i, revealing all of A_i (truthfulness)
    is a best response against every possible combination of reports from other agents:
        forall i, forall R_{-i}, forall S_i subseteq A_i: u_i(A_i, R_{-i}) >= u_i(S_i, R_{-i}).

    Args:
        global_af: The global argumentation framework.
        partition: Mapping of agent_id -> owned arguments A_i.
        cache: Optional precomputed grounded cache for argument subsets.

    Returns:
        (True, None) if strategyproof.
        (False, counterexample_dict) if strategyproofness fails.
    """
    if cache is None:
        cache = precompute_grounded_cache(global_af)

    agents = list(partition.keys())

    # Pre-generate powerset of each agent's owned arguments
    agent_powersets = {i: list(powerset(partition[i])) for i in agents}

    for i in agents:
        A_i = partition[i]
        other_agents = [j for j in agents if j != i]

        # Generate all profiles of reports from other agents: product of powersets
        if other_agents:
            other_profiles_iter = product(*[agent_powersets[j] for j in other_agents])
        else:
            other_profiles_iter = [()]

        for other_combo in other_profiles_iter:
            other_reports = {
                other_agents[idx]: other_combo[idx]
                for idx in range(len(other_agents))
            }
            other_revealed = set().union(*other_reports.values()) if other_reports else set()

            # Truthful report for agent i
            truthful_revealed = frozenset(other_revealed | A_i)
            truthful_outcome = cache[truthful_revealed]
            truthful_util = agent_utility(A_i, truthful_outcome)

            # Test every deviation S_i subseteq A_i
            for deviation in agent_powersets[i]:
                dev_revealed = frozenset(other_revealed | deviation)
                dev_outcome = cache[dev_revealed]
                dev_util = agent_utility(A_i, dev_outcome)

                if dev_util > truthful_util:
                    # Strategyproofness violated: agent i strictly benefits by deviating!
                    counterexample = {
                        "agent": i,
                        "A_i": sorted(list(A_i), key=lambda x: str(x)),
                        "other_reports": {
                            str(k): sorted(list(v), key=lambda x: str(x))
                            for k, v in other_reports.items()
                        },
                        "truthful_report": sorted(list(A_i), key=lambda x: str(x)),
                        "deviation_report": sorted(list(deviation), key=lambda x: str(x)),
                        "hidden_arguments": sorted(list(A_i - deviation), key=lambda x: str(x)),
                        "truthful_utility": truthful_util,
                        "deviation_utility": dev_util,
                        "truthful_outcome": sorted(list(truthful_outcome), key=lambda x: str(x)),
                        "deviation_outcome": sorted(list(dev_outcome), key=lambda x: str(x)),
                    }
                    return False, counterexample

    return True, None


def odd_reachable_walks(
    af: ArgumentationFramework, start: Any
) -> Dict[Any, List[Any]]:
    """Find all targets reachable from start via an odd-length directed walk
    using parity-aware BFS on the 2-state graph (vertex, parity).

    Returns:
        Dict mapping target_node -> path_witness (list of nodes forming the walk).
    """
    # State: (node, parity) where parity 0 = even, 1 = odd
    # queue stores (node, parity, path_so_far)
    queue = deque([(start, 0, [start])])
    visited = {(start, 0)}
    odd_witnesses: Dict[Any, List[Any]] = {}

    while queue:
        node, parity, path = queue.popleft()
        for nxt in af.targets[node]:
            next_parity = 1 - parity
            next_path = path + [nxt]

            if next_parity == 1 and nxt not in odd_witnesses:
                odd_witnesses[nxt] = next_path

            state = (nxt, next_parity)
            if state not in visited:
                visited.add(state)
                queue.append((nxt, next_parity, next_path))

    return odd_witnesses


def find_odd_simple_path(
    af: ArgumentationFramework, start: Any, target: Any
) -> Optional[List[Any]]:
    """Find a simple directed path of odd length from start to target.

    If start == target, searches for an odd-length simple directed cycle
    (where vertices 0..k-1 are distinct and vertex k == start).

    Returns:
        List of arguments forming the path/cycle if found, else None.
    """
    def dfs(current: Any, visited: Set[Any], current_path: List[Any]) -> Optional[List[Any]]:
        for nxt in af.targets[current]:
            edge_len = len(current_path)  # length of path to nxt is len(current_path)
            if nxt == target and (edge_len % 2 == 1):
                return current_path + [nxt]
            if nxt not in visited:
                visited.add(nxt)
                result = dfs(nxt, visited, current_path + [nxt])
                if result is not None:
                    return result
                visited.remove(nxt)
        return None

    visited_set = {start} if start != target else set()
    return dfs(start, visited_set, [start])


def check_theorem_5_4(
    global_af: ArgumentationFramework,
    partition: Dict[Any, Set[Any]],
    use_simple_path: bool = False
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """Verify Theorem 5.4: Structural Sufficient Condition for Strategyproofness.

    Theorem 5.4 states that a grounded direct argumentation mechanism is strategyproof
    if NO agent holds two arguments alpha, beta such that there is an odd-length
    directed path (or walk) from alpha to beta in the full graph.
    (Includes alpha == beta for self-attacks or odd directed cycles).

    Args:
        global_af: The global argumentation framework.
        partition: Mapping of agent_id -> owned arguments A_i.
        use_simple_path: If True, requires simple directed paths; if False (default),
                         uses parity-aware BFS for directed walks (as described in prompt).

    Returns:
        (True, None) if condition holds (no odd self-defeat exists).
        (False, violation_dict) if condition fails.
    """
    for agent_id, A_i in partition.items():
        if not A_i:
            continue

        if not use_simple_path:
            # Parity-aware BFS for each starting node in A_i
            for alpha in A_i:
                odd_targets = odd_reachable_walks(global_af, alpha)
                # Check if any beta in A_i is in odd_targets
                for beta in A_i:
                    if beta in odd_targets:
                        witness = odd_targets[beta]
                        return False, {
                            "agent": agent_id,
                            "alpha": alpha,
                            "beta": beta,
                            "path": [str(x) for x in witness],
                            "length": len(witness) - 1,
                            "is_cycle": (alpha == beta),
                            "mode": "parity_walk",
                        }
        else:
            # Simple path search
            for alpha in A_i:
                for beta in A_i:
                    path = find_odd_simple_path(global_af, alpha, beta)
                    if path is not None:
                        return False, {
                            "agent": agent_id,
                            "alpha": alpha,
                            "beta": beta,
                            "path": [str(x) for x in path],
                            "length": len(path) - 1,
                            "is_cycle": (alpha == beta),
                            "mode": "simple_path",
                        }

    return True, None
