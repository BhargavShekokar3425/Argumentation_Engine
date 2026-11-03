"""
Argumentation Framework representation module.

Defines the core ArgumentationFramework class that models an abstract
argumentation framework AF = <A, R>, with arguments A and directed attack
relation R subseteq A x A.
"""

from typing import Set, Tuple, Dict, Any, Iterable, Optional


class ArgumentationFramework:
    """Represents an Abstract Argumentation Framework AF = (A, R).

    Attributes:
        arguments: Set of argument identifiers.
        attacks: Set of directed attack pairs (attacker, target).
        attackers: Dict mapping an argument to the set of arguments attacking it.
        targets: Dict mapping an argument to the set of arguments it attacks.
    """

    def __init__(
        self,
        arguments: Iterable[Any],
        attacks: Iterable[Tuple[Any, Any]],
        validate: bool = True
    ) -> None:
        """Initialize an argumentation framework.

        Args:
            arguments: Iterable of argument identifiers.
            attacks: Iterable of (attacker, target) pairs.
            validate: Whether to validate that attack endpoints exist in arguments.

        Raises:
            ValueError: If an attack references an argument not in arguments.
        """
        self.arguments: Set[Any] = set(arguments)
        self.attacks: Set[Tuple[Any, Any]] = set(attacks)

        if validate:
            for src, dst in self.attacks:
                if src not in self.arguments:
                    raise ValueError(f"Attack source '{src}' is not in arguments.")
                if dst not in self.arguments:
                    raise ValueError(f"Attack target '{dst}' is not in arguments.")

        self.attackers: Dict[Any, Set[Any]] = {a: set() for a in self.arguments}
        self.targets: Dict[Any, Set[Any]] = {a: set() for a in self.arguments}

        for src, dst in self.attacks:
            self.targets[src].add(dst)
            self.attackers[dst].add(src)

    def induced_subgraph(self, subset: Iterable[Any]) -> "ArgumentationFramework":
        """Return the induced argumentation framework restricted to the given subset.

        Args:
            subset: Arguments to keep.

        Returns:
            A new ArgumentationFramework with arguments subset and all attacks
            between them.
        """
        sub_args = set(subset) & self.arguments
        sub_attacks = {
            (src, dst)
            for src, dst in self.attacks
            if src in sub_args and dst in sub_args
        }
        return ArgumentationFramework(sub_args, sub_attacks, validate=False)

    def is_unattacked(self, argument: Any) -> bool:
        """Check if an argument has no attackers."""
        return len(self.attackers[argument]) == 0

    def attackers_of(self, argument: Any) -> Set[Any]:
        """Return the set of arguments directly attacking the given argument."""
        return self.attackers.get(argument, set())

    def targets_of(self, argument: Any) -> Set[Any]:
        """Return the set of arguments directly attacked by the given argument."""
        return self.targets.get(argument, set())

    def attacks_set(self, argument_set: Set[Any]) -> Set[Any]:
        """Return the set S^+ of all arguments attacked by any argument in argument_set."""
        attacked = set()
        for a in argument_set:
            attacked.update(self.targets[a])
        return attacked

    def __len__(self) -> int:
        return len(self.arguments)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ArgumentationFramework):
            return False
        return self.arguments == other.arguments and self.attacks == other.attacks

    def __hash__(self) -> int:
        return hash((frozenset(self.arguments), frozenset(self.attacks)))

    def __repr__(self) -> str:
        sorted_args = sorted(list(self.arguments), key=lambda x: str(x))
        sorted_attacks = sorted(list(self.attacks), key=lambda x: (str(x[0]), str(x[1])))
        return f"ArgumentationFramework(arguments={sorted_args}, attacks={sorted_attacks})"

    def to_dict(self) -> Dict[str, Any]:
        """Convert framework to a serializable dictionary."""
        return {
            "arguments": sorted([str(a) for a in self.arguments]),
            "attacks": sorted([[str(u), str(v)] for u, v in self.attacks]),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ArgumentationFramework":
        """Reconstruct framework from dictionary."""
        arguments = set(data["arguments"])
        attacks = set((u, v) for u, v in data["attacks"])
        return cls(arguments, attacks)
