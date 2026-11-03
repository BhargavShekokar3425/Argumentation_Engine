"""
Canonical Textbook Examples from the Argumentation Literature.

Includes:
1. Three-argument running example (mutual attack + defense).
2. Directed 3-cycle (odd cycle, no stable extensions).
3. Strategic manipulation example (Example 5.10 / Rahwan & Larson).
   - Explicitly notes the textbook misprint where utilities of y and z were swapped.
4. Protected indirect-defeat example (Discussion after Example 5.11).
   - Explicitly notes the textbook misprint where the protecting argument is alpha_6, not alpha_5.
   - Demonstrates that Theorem 5.4 is sufficient, but NOT necessary!
"""

from typing import Dict, Any, Tuple
from argumentation.framework import ArgumentationFramework
from argumentation.semantics import compute_all_extensions
from argumentation.labelling import compute_legal_labellings
from argumentation.acceptance import argument_acceptance_status
from argumentation.mechanism import grounded_direct_mechanism, agent_utility, compute_best_responses
from argumentation.strategyproof import check_theorem_5_3, check_theorem_5_4


def example_running_three_arg() -> Tuple[ArgumentationFramework, Dict[str, Any]]:
    """Introductory 3-argument example:
    Arguments: {a, b, c}
    Attacks: (a, b), (b, a), (b, c)

    Results:
    - Grounded: {}
    - Complete: {}, {a, c}, {b}
    - Preferred: {a, c}, {b}
    - Stable: {a, c}, {b}
    - Semi-stable: {a, c}, {b}
    """
    af = ArgumentationFramework(
        arguments={"a", "b", "c"},
        attacks={("a", "b"), ("b", "a"), ("b", "c")}
    )
    exts = compute_all_extensions(af)
    labs = compute_legal_labellings(af, exts["complete"])
    status_a = argument_acceptance_status(af, "a", "preferred", exts["preferred"])

    return af, {
        "extensions": exts,
        "labellings": labs,
        "status_a_preferred": status_a,
    }


def example_three_cycle() -> Tuple[ArgumentationFramework, Dict[str, Any]]:
    """Directed 3-cycle:
    Arguments: {a, b, c}
    Attacks: (a, b), (b, c), (c, a)

    Important behavior:
    - Grounded: {}
    - Complete: [{}]
    - Preferred: [{}]
    - Stable: [] (NO stable extension exists!)
    - Semi-stable: [{}]
    """
    af = ArgumentationFramework(
        arguments={"a", "b", "c"},
        attacks={("a", "b"), ("b", "c"), ("c", "a")}
    )
    exts = compute_all_extensions(af)
    status_a_stable = argument_acceptance_status(af, "a", "stable", exts["stable"])

    return af, {
        "extensions": exts,
        "status_a_stable": status_a_stable,
    }


def example_strategic_manipulation_5_10() -> Dict[str, Any]:
    """Example 5.10 from textbook (Strategic Argumentation Manipulation).

    Arguments: {1, 2, 3, 4, 5}
    Attacks: 1 -> 2 -> 3 -> 4, and 3 -> 5.
    Agents:
      - Agent X: {1, 4, 5}
      - Agent Y: {2}
      - Agent Z: {3}

    Truthful reporting:
      Revealed: {1, 2, 3, 4, 5}
      Grounded outcome: {1, 3}
      Utility X: |{1, 4, 5} intersect {1, 3}| = 1
      Utility Y: |{2} intersect {1, 3}| = 0
      Utility Z: |{3} intersect {1, 3}| = 1

    [TEXTBOOK MISPRINT NOTE]:
    In textbook Example 5.10, the utilities of y and z were accidentally swapped in the text.
    Here correctly: Agent Y utility = 0, Agent Z utility = 1.

    Manipulation by Agent X:
      Agent X hides 1 (reports {4, 5}).
      Revealed: {2, 3, 4, 5}
      Grounded outcome: {2, 4, 5}
      Utility X: |{1, 4, 5} intersect {2, 4, 5}| = 2 (Utility increased from 1 to 2!)

    Theorem 5.3 check: FAILS (not strategyproof).
    Theorem 5.4 check: FAILS (Agent X owns 1 and 4, path 1 -> 2 -> 3 -> 4 is length 3, odd).
    """
    af = ArgumentationFramework(
        arguments={"1", "2", "3", "4", "5"},
        attacks={("1", "2"), ("2", "3"), ("3", "4"), ("3", "5")}
    )
    partition = {
        "X": {"1", "4", "5"},
        "Y": {"2"},
        "Z": {"3"}
    }

    # Truthful profiles
    truthful_reports = {agent: set(args) for agent, args in partition.items()}
    truthful_outcome = grounded_direct_mechanism(af, truthful_reports)
    truthful_utilities = {
        agent: agent_utility(args, truthful_outcome)
        for agent, args in partition.items()
    }

    # Agent X manipulates: hides "1"
    manipulated_reports = {
        "X": {"4", "5"},
        "Y": {"2"},
        "Z": {"3"}
    }
    manipulated_outcome = grounded_direct_mechanism(af, manipulated_reports)
    manipulated_utilities = {
        agent: agent_utility(partition[agent], manipulated_outcome)
        for agent in partition
    }

    is_sp, ce = check_theorem_5_3(af, partition)
    cond_holds, witness = check_theorem_5_4(af, partition)

    return {
        "framework": af,
        "partition": partition,
        "truthful_outcome": truthful_outcome,
        "truthful_utilities": truthful_utilities,
        "manipulated_reports": manipulated_reports,
        "manipulated_outcome": manipulated_outcome,
        "manipulated_utilities": manipulated_utilities,
        "is_strategyproof_thm_5_3": is_sp,
        "counterexample": ce,
        "condition_holds_thm_5_4": cond_holds,
        "odd_path_witness": witness,
    }


def example_protected_indirect_defeat_5_11() -> Dict[str, Any]:
    """Protected Indirect-Defeat Example (Discussion after Example 5.11).

    Extends Example 5.10 by giving Agent X an additional argument '6' which attacks '3'.
    [TEXTBOOK MISPRINT NOTE]:
    The textbook discussion after Example 5.11 accidentally referred to this argument as alpha_5
    instead of alpha_6. Here alpha_6 is the new protecting argument.

    Arguments: {1, 2, 3, 4, 5, 6}
    Attacks: 1 -> 2 -> 3 -> 4, 3 -> 5, and 6 -> 3.
    Agents:
      - Agent X: {1, 4, 5, 6}
      - Agent Y: {2}
      - Agent Z: {3}

    Structural condition (Theorem 5.4):
      Agent X owns 1 and 4, and the odd path 1 -> 2 -> 3 -> 4 of length 3 STILL EXISTS!
      Therefore, Theorem 5.4's condition FAILS (condition_holds = False).

    Exact Strategyproofness (Theorem 5.3):
      Argument 6 is unattacked, so under truthfulness 6 is always accepted.
      6 defeats 3, allowing 4 and 5 to be accepted.
      Under truthfulness, Agent X gets {1, 4, 5, 6} all accepted, achieving utility 4 (the maximum possible!).
      No deviation can give > 4.
      In fact, exhaustive verification shows the mechanism IS STRATEGYPROOF!

    Conclusion:
      This is an empirical proof that Theorem 5.4 is a SUFFICIENT condition, NOT a necessary condition!
    """
    af = ArgumentationFramework(
        arguments={"1", "2", "3", "4", "5", "6"},
        attacks={("1", "2"), ("2", "3"), ("3", "4"), ("3", "5"), ("6", "3")}
    )
    partition = {
        "X": {"1", "4", "5", "6"},
        "Y": {"2"},
        "Z": {"3"}
    }

    is_sp, ce = check_theorem_5_3(af, partition)
    cond_holds, witness = check_theorem_5_4(af, partition)

    truthful_reports = {agent: set(args) for agent, args in partition.items()}
    truthful_outcome = grounded_direct_mechanism(af, truthful_reports)
    truthful_utilities = {
        agent: agent_utility(args, truthful_outcome)
        for agent, args in partition.items()
    }

    return {
        "framework": af,
        "partition": partition,
        "truthful_outcome": truthful_outcome,
        "truthful_utilities": truthful_utilities,
        "is_strategyproof_thm_5_3": is_sp,
        "counterexample": ce,
        "condition_holds_thm_5_4": cond_holds,
        "odd_path_witness": witness,
    }


if __name__ == "__main__":
    print("=== Running 3-argument example ===")
    _, res1 = example_running_three_arg()
    print("Grounded:", res1["extensions"]["grounded"])
    print("Complete:", res1["extensions"]["complete"])
    print("Preferred:", res1["extensions"]["preferred"])
    print("Stable:", res1["extensions"]["stable"])
    print("Labellings:", res1["labellings"])
    print("Acceptance of 'a' under preferred:", res1["status_a_preferred"]["status"])

    print("\n=== Strategic Manipulation Example 5.10 ===")
    res_man = example_strategic_manipulation_5_10()
    print("Truthful GE:", res_man["truthful_outcome"])
    print("Truthful Utilities:", res_man["truthful_utilities"])
    print("Manipulated GE (X hides 1):", res_man["manipulated_outcome"])
    print("Manipulated Utilities:", res_man["manipulated_utilities"])
    print("Thm 5.3 (Strategyproof):", res_man["is_strategyproof_thm_5_3"])
    print("Thm 5.4 (Odd-path condition holds):", res_man["condition_holds_thm_5_4"])

    print("\n=== Protected Indirect-Defeat Example 5.11 (alpha_6) ===")
    res_prot = example_protected_indirect_defeat_5_11()
    print("Truthful Utilities:", res_prot["truthful_utilities"])
    print("Thm 5.3 (Strategyproof):", res_prot["is_strategyproof_thm_5_3"])
    print("Thm 5.4 (Odd-path condition holds):", res_prot["condition_holds_thm_5_4"])
    print("Odd path witness:", res_prot["odd_path_witness"])
