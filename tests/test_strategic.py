"""
Unit tests for Strategic Argumentation, Theorems 5.3 and 5.4,
and manipulation counterexamples.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from argumentation.framework import ArgumentationFramework
from argumentation.mechanism import (
    grounded_direct_mechanism,
    agent_utility,
    compute_best_responses,
)
from argumentation.strategyproof import (
    check_theorem_5_3,
    check_theorem_5_4,
    find_odd_simple_path,
    odd_reachable_walks,
)
from examples.textbook_examples import (
    example_strategic_manipulation_5_10,
    example_protected_indirect_defeat_5_11,
)


class TestStrategicArgumentation(unittest.TestCase):

    def test_example_5_10_manipulation(self):
        res = example_strategic_manipulation_5_10()

        # Check truthful utilities (noting textbook misprint fix)
        self.assertEqual(res["truthful_utilities"]["X"], 1)
        self.assertEqual(res["truthful_utilities"]["Y"], 0)
        self.assertEqual(res["truthful_utilities"]["Z"], 1)

        # Check manipulated utilities (X hides 1)
        self.assertEqual(res["manipulated_utilities"]["X"], 2)

        # Strategyproofness fails
        self.assertFalse(res["is_strategyproof_thm_5_3"])
        self.assertIsNotNone(res["counterexample"])
        self.assertEqual(res["counterexample"]["agent"], "X")

        # Theorem 5.4 condition fails
        self.assertFalse(res["condition_holds_thm_5_4"])
        self.assertEqual(res["odd_path_witness"]["length"], 3)

    def test_best_responses_example_5_10(self):
        af = ArgumentationFramework(
            arguments={"1", "2", "3", "4", "5"},
            attacks={("1", "2"), ("2", "3"), ("3", "4"), ("3", "5")}
        )
        partition = {
            "X": {"1", "4", "5"},
            "Y": {"2"},
            "Z": {"3"}
        }
        # When Y reports {2} and Z reports {3}:
        other_reports = {"Y": {"2"}, "Z": {"3"}}
        max_u, best_reports, truthful_u, is_truthful = compute_best_responses(
            af, "X", partition, other_reports
        )
        self.assertEqual(truthful_u, 1)
        self.assertEqual(max_u, 2)
        self.assertFalse(is_truthful)
        # Any report hiding 1 while revealing {4, 5} or similar
        self.assertIn({"4", "5"}, best_reports)

    def test_protected_indirect_defeat_5_11(self):
        res = example_protected_indirect_defeat_5_11()

        # Theorem 5.4 fails because path 1 -> 2 -> 3 -> 4 still exists
        self.assertFalse(res["condition_holds_thm_5_4"])

        # BUT Theorem 5.3 holds because alpha_6 protects X's arguments!
        self.assertTrue(res["is_strategyproof_thm_5_3"])
        self.assertIsNone(res["counterexample"])

        # Truthful utility is 4
        self.assertEqual(res["truthful_utilities"]["X"], 4)

    def test_cycle_odd_path_detection(self):
        # Directed 3-cycle: a -> b -> c -> a
        af = ArgumentationFramework(
            arguments={"a", "b", "c"},
            attacks={("a", "b"), ("b", "c"), ("c", "a")}
        )
        # Parity walk from a to a: length 3 (odd cycle)
        odd_w = odd_reachable_walks(af, "a")
        self.assertIn("a", odd_w)
        self.assertEqual(len(odd_w["a"]) - 1, 3)

        # Simple path from a to a (cycle): length 3
        path = find_odd_simple_path(af, "a", "a")
        self.assertIsNotNone(path)
        self.assertEqual(len(path) - 1, 3)

    def test_self_attack_detection(self):
        # Self-attack is an odd cycle of length 1
        af = ArgumentationFramework({"x"}, {("x", "x")})
        cond, witness = check_theorem_5_4(af, {"agent_1": {"x"}})
        self.assertFalse(cond)
        self.assertEqual(witness["alpha"], "x")
        self.assertEqual(witness["beta"], "x")
        self.assertEqual(witness["length"], 1)

    def test_trivial_strategyproof_instances(self):
        # Framework with no attacks is trivially strategyproof
        af_no_attacks = ArgumentationFramework({"a", "b", "c"}, set())
        partition = {"1": {"a"}, "2": {"b"}, "3": {"c"}}
        is_sp, ce = check_theorem_5_3(af_no_attacks, partition)
        self.assertTrue(is_sp)
        cond, witness = check_theorem_5_4(af_no_attacks, partition)
        self.assertTrue(cond)


if __name__ == "__main__":
    unittest.main()
