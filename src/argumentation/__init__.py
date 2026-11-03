"""
Argumentation Engine Package.

Provides complete tools for:
- Abstract Argumentation Frameworks
- Defense, Conflict-freeness, Admissibility
- All Semantics (Grounded, Complete, Preferred, Stable, Semi-stable)
- Caminada 3-valued Labellings (IN / OUT / UNDEC)
- Skeptical / Credulous / Rejected Acceptance Status
- Strategic Argumentation Mechanisms (Grounded Direct Mechanism)
- Theorem 5.3 (Strategyproofness Verification)
- Theorem 5.4 (Odd-path structural condition verification)
- Random Framework & Partition Generator
"""

from .framework import ArgumentationFramework
from .defense import (
    is_conflict_free,
    defends,
    characteristic,
    is_admissible,
    is_complete,
)
from .semantics import (
    compute_grounded,
    compute_complete,
    compute_preferred,
    compute_stable,
    compute_semi_stable,
    compute_all_extensions,
)
from .labelling import (
    Labelling,
    compute_legal_labellings,
    is_legal_labelling,
    labelling_from_complete_extension,
)
from .acceptance import (
    argument_acceptance_status,
    get_extensions_for_semantics,
)
from .mechanism import (
    grounded_direct_mechanism,
    agent_utility,
    compute_best_responses,
)
from .strategyproof import (
    check_theorem_5_3,
    check_theorem_5_4,
    precompute_grounded_cache,
    odd_reachable_walks,
    find_odd_simple_path,
)
from .graph_generator import (
    generate_random_af,
    random_agent_partition,
)

__all__ = [
    "ArgumentationFramework",
    "is_conflict_free",
    "defends",
    "characteristic",
    "is_admissible",
    "is_complete",
    "compute_grounded",
    "compute_complete",
    "compute_preferred",
    "compute_stable",
    "compute_semi_stable",
    "compute_all_extensions",
    "Labelling",
    "compute_legal_labellings",
    "is_legal_labelling",
    "labelling_from_complete_extension",
    "argument_acceptance_status",
    "get_extensions_for_semantics",
    "grounded_direct_mechanism",
    "agent_utility",
    "compute_best_responses",
    "check_theorem_5_3",
    "check_theorem_5_4",
    "precompute_grounded_cache",
    "odd_reachable_walks",
    "find_odd_simple_path",
    "generate_random_af",
    "random_agent_partition",
]
