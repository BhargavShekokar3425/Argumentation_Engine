"""
Unit tests for Caminada labellings and skeptical/credulous acceptance status.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from argumentation.framework import ArgumentationFramework
from argumentation.semantics import compute_complete
from argumentation.labelling import (
    Labelling,
    compute_legal_labellings,
    is_legal_labelling,
)
from argumentation.acceptance import argument_acceptance_status


class TestLabellingAndAcceptance(unittest.TestCase):

    def setUp(self):
        # Running example: a <-> b, b -> c
        self.af = ArgumentationFramework(
            arguments={"a", "b", "c"},
            attacks={("a", "b"), ("b", "a"), ("b", "c")}
        )

    def test_running_example_labellings(self):
        labellings = compute_legal_labellings(self.af)
        self.assertEqual(len(labellings), 3)

        # Verify each labelling is valid according to Caminada conditions
        for lab in labellings:
            self.assertTrue(is_legal_labelling(self.af, lab))

        # Expected labellings:
        # 1. IN={}, OUT={}, UNDEC={a, b, c}
        # 2. IN={a, c}, OUT={b}, UNDEC={}
        # 3. IN={b}, OUT={a, c}, UNDEC={}
        expected_sets = {
            (frozenset(), frozenset(), frozenset({"a", "b", "c"})),
            (frozenset({"a", "c"}), frozenset({"b"}), frozenset()),
            (frozenset({"b"}), frozenset({"a", "c"}), frozenset()),
        }
        actual_sets = {
            (frozenset(l.in_set), frozenset(l.out_set), frozenset(l.undec_set))
            for l in labellings
        }
        self.assertEqual(actual_sets, expected_sets)

    def test_illegal_labelling_detection(self):
        # IN={a}, OUT={}, UNDEC={b, c} is illegal because b attacks a but b is not OUT
        illegal = Labelling(in_set={"a"}, out_set=set(), undec_set={"b", "c"})
        self.assertFalse(is_legal_labelling(self.af, illegal))

    def test_acceptance_status_running_example(self):
        # Under preferred semantics: extensions are {a, c} and {b}
        status_a = argument_acceptance_status(self.af, "a", semantics="preferred")
        self.assertEqual(status_a["status"], "credulous_only")
        self.assertTrue(status_a["is_credulous"])
        self.assertFalse(status_a["is_skeptical"])

        status_b = argument_acceptance_status(self.af, "b", semantics="preferred")
        self.assertEqual(status_b["status"], "credulous_only")

        status_c = argument_acceptance_status(self.af, "c", semantics="preferred")
        self.assertEqual(status_c["status"], "credulous_only")

        # Under grounded semantics: extension is {}
        status_a_g = argument_acceptance_status(self.af, "a", semantics="grounded")
        self.assertEqual(status_a_g["status"], "rejected")

    def test_acceptance_status_chain(self):
        # 1 -> 2 -> 3
        af = ArgumentationFramework({"1", "2", "3"}, {("1", "2"), ("2", "3")})
        # Preferred extension is unique: {1, 3}
        status_1 = argument_acceptance_status(af, "1", "preferred")
        self.assertEqual(status_1["status"], "skeptical")

        status_2 = argument_acceptance_status(af, "2", "preferred")
        self.assertEqual(status_2["status"], "rejected")

        status_3 = argument_acceptance_status(af, "3", "preferred")
        self.assertEqual(status_3["status"], "skeptical")

    def test_acceptance_status_empty_stable(self):
        # Directed 3-cycle: stable has no extensions
        af = ArgumentationFramework({"x", "y", "z"}, {("x", "y"), ("y", "z"), ("z", "x")})
        status_x = argument_acceptance_status(af, "x", "stable")
        # Must NOT be skeptically accepted by vacuous truth
        self.assertEqual(status_x["status"], "rejected")
        self.assertFalse(status_x["is_skeptical"])
        self.assertEqual(status_x["num_extensions"], 0)


if __name__ == "__main__":
    unittest.main()
