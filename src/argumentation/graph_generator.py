"""
Random Argumentation Framework and Agent Partition Generator.

Generates random directed attack graphs according to the Erdős-Rényi model
G(n, p) on directed edges, and randomly partitions arguments among agents.
"""

import random
from typing import Set, Tuple, Dict, List, Any, Optional, Iterable
from .framework import ArgumentationFramework


def generate_random_af(
    num_arguments: int,
    attack_probability: float,
    allow_self_attacks: bool = True,
    seed: Optional[int] = None,
    arg_prefix: str = "a"
) -> ArgumentationFramework:
    """Generate a random argumentation framework AF = (A, R).

    For each ordered pair (u, v) in A x A, an attack (u, v) is added
    independently with probability attack_probability.

    Args:
        num_arguments: Total number of arguments n.
        attack_probability: Probability p in [0, 1] for each directed edge.
        allow_self_attacks: Whether self-attacks (u, u) are permitted.
        seed: Random seed for reproducibility.
        arg_prefix: Prefix string for argument names.

    Returns:
        ArgumentationFramework instance.
    """
    if seed is not None:
        random.seed(seed)

    arguments = [f"{arg_prefix}{i+1}" for i in range(num_arguments)]
    attacks: Set[Tuple[str, str]] = set()

    for u in arguments:
        for v in arguments:
            if u == v and not allow_self_attacks:
                continue
            if random.random() < attack_probability:
                attacks.add((u, v))

    return ArgumentationFramework(arguments, attacks, validate=False)


def random_agent_partition(
    arguments: Iterable[Any],
    num_agents: int = 3,
    ensure_non_empty: bool = True,
    seed: Optional[int] = None,
    agent_names: Optional[List[str]] = None
) -> Dict[str, Set[Any]]:
    """Partition arguments uniformly at random among agents.

    Args:
        arguments: Set or list of arguments.
        num_agents: Number of agents (default 3).
        ensure_non_empty: If True, guarantees each agent receives at least 1 argument
                          when len(arguments) >= num_agents.
        seed: Random seed for reproducibility.
        agent_names: Optional list of agent names.

    Returns:
        Dict mapping agent_name -> Set[arguments].
    """
    if seed is not None:
        random.seed(seed)

    args = list(arguments)
    if agent_names is None:
        agent_names = [f"agent_{i+1}" for i in range(num_agents)]

    partition: Dict[str, Set[Any]] = {name: set() for name in agent_names}

    if ensure_non_empty and len(args) >= num_agents:
        shuffled = args.copy()
        random.shuffle(shuffled)
        # Give 1 argument to each agent first
        for i in range(num_agents):
            partition[agent_names[i]].add(shuffled[i])
        # Distribute remaining arguments uniformly
        for arg in shuffled[num_agents:]:
            chosen = random.choice(agent_names)
            partition[chosen].add(arg)
    else:
        for arg in args:
            chosen = random.choice(agent_names)
            partition[chosen].add(arg)

    return partition
