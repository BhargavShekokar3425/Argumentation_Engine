"""
Unit tests for Argumentation Framework, conflict-freeness, defense,
and the characteristic function.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from argumentation.framework import ArgumentationFramework
from argumentation.defense import (
    is_conflict_free,
    defends,
    characteristic,
    is_admissible,
    is_complete,
)


class TestArgumentationFramework(unittest.TestCase):

    def setUp(self):
        # Running example: a <-> b, b -> c
        self.af = ArgumentationFramework(
            arguments={"a", "b", "c"},
            attacks={("a", "b"), ("b", "a"), ("b", "c")}
        )

    def test_initialization_and_validation(self):
        self.assertEqual(self.af.arguments, {"a", "b", "c"})
        self.assertEqual(len(self.af.attacks), 3)
        self.assertEqual(self.af.attackers["a"], {"b"})
        self.assertEqual(self.af.targets["a"], {"b"})
        self.assertEqual(self.af.attackers["c"], {"b"})
        self.assertEqual(self.af.targets["c"], set())

        # Validation should reject invalid endpoints
        with self.assertRaises(ValueError):
            ArgumentationFramework({"a", "b"}, {("a", "z")})
        with self.assertRaises(ValueError):
            ArgumentationFramework({"a", "b"}, {("z", "b")})

    def test_induced_subgraph(self):
        sub = self.af.induced_subgraph({"b", "c"})
        self.assertEqual(sub.arguments, {"b", "c"})
        self.assertEqual(sub.attacks, {("b", "c")})
        self.assertEqual(sub.attackers["b"], set())
        self.assertEqual(sub.targets["b"], {"c"})

    def test_conflict_free(self):
        # Empty set is conflict-free
        self.assertTrue(is_conflict_free(self.af, set()))
        # Singletons
        self.assertTrue(is_conflict_free(self.af, {"a"}))
        self.assertTrue(is_conflict_free(self.af, {"b"}))
        self.assertTrue(is_conflict_free(self.af, {"c"}))
        # Non-conflicting pairs
        self.assertTrue(is_conflict_free(self.af, {"a", "c"}))
        # Conflicting pairs
        self.assertFalse(is_conflict_free(self.af, {"a", "b"}))
        self.assertFalse(is_conflict_free(self.af, {"b", "c"}))
        self.assertFalse(is_conflict_free(self.af, {"a", "b", "c"}))

    def test_self_attack_conflict(self):
        af_self = ArgumentationFramework({"x"}, {("x", "x")})
        self.assertFalse(is_conflict_free(af_self, {"x"}))
        self.assertTrue(is_conflict_free(af_self, set()))

    def test_defends(self):
        # Unattacked argument is defended by any set (including empty set)
        af_chain = ArgumentationFramework({"1", "2"}, {("1", "2")})
        self.assertTrue(defends(af_chain, set(), "1"))
        self.assertFalse(defends(af_chain, set(), "2"))
        self.assertFalse(defends(af_chain, {"2"}, "2"))

        # In running example:
        # {a} attacks b, which is the only attacker of c -> {a} defends c
        self.assertTrue(defends(self.af, {"a"}, "c"))
        self.assertTrue(defends(self.af, {"a"}, "a"))
        self.assertFalse(defends(self.af, {"c"}, "a"))
        self.assertFalse(defends(self.af, set(), "a"))
        self.assertFalse(defends(self.af, set(), "b"))
        self.assertFalse(defends(self.af, set(), "c"))

    def test_characteristic_function(self):
        # F({}) = {}
        self.assertEqual(characteristic(self.af, set()), set())
        # F({a}) = {a, c}
        self.assertEqual(characteristic(self.af, {"a"}), {"a", "c"})
        # F({b}) = {b}
        self.assertEqual(characteristic(self.af, {"b"}), {"b"})
        # F({c}) = {}
        self.assertEqual(characteristic(self.af, {"c"}), set())

    def test_admissible_and_complete(self):
        # Empty set is admissible
        self.assertTrue(is_admissible(self.af, set()))
        # {a} is admissible (F({a}) = {a, c} contains {a})
        self.assertTrue(is_admissible(self.af, {"a"}))
        # {a, c} is admissible (F({a, c}) = {a, c})
        self.assertTrue(is_admissible(self.af, {"a", "c"}))
        # {b} is admissible
        self.assertTrue(is_admissible(self.af, {"b"}))
        # {c} is NOT admissible (not defended by {c})
        self.assertFalse(is_admissible(self.af, {"c"}))
        # {a, b} is NOT admissible (conflict)
        self.assertFalse(is_admissible(self.af, {"a", "b"}))

        # Complete extensions:
        # {} is complete: F({}) = {} and conflict-free
        self.assertTrue(is_complete(self.af, set()))
        # {a} is NOT complete: F({a}) = {a, c} != {a}
        self.assertFalse(is_complete(self.af, {"a"}))
        # {a, c} is complete: F({a, c}) = {a, c}
        self.assertTrue(is_complete(self.af, {"a", "c"}))
        # {b} is complete: F({b}) = {b}
        self.assertTrue(is_complete(self.af, {"b"}))


if __name__ == "__main__":
    unittest.main()
