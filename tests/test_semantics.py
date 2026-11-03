"""
Unit tests for Argumentation Semantics:
- Grounded
- Complete
- Preferred
- Stable
- Semi-stable
And validation of foundational theoretical relationships.
"""

import unittest
from argumentation.framework import ArgumentationFramework
from argumentation.semantics import (
    compute_grounded,
    compute_complete,
    compute_preferred,
    compute_stable,
    compute_semi_stable,
    compute_all_extensions,
)


class TestArgumentationSemantics(unittest.TestCase):

    def test_running_example(self):
        # a <-> b, b -> c
        af = ArgumentationFramework(
            arguments={"a", "b", "c"},
            attacks={("a", "b"), ("b", "a"), ("b", "c")}
        )
        exts = compute_all_extensions(af)

        self.assertEqual(exts["grounded"], set())
        self.assertEqual(
            set(map(frozenset, exts["complete"])),
            {frozenset(), frozenset({"a", "c"}), frozenset({"b"})}
        )
        self.assertEqual(
            set(map(frozenset, exts["preferred"])),
            {frozenset({"a", "c"}), frozenset({"b"})}
        )
        self.assertEqual(
            set(map(frozenset, exts["stable"])),
            {frozenset({"a", "c"}), frozenset({"b"})}
        )
        self.assertEqual(
            set(map(frozenset, exts["semi_stable"])),
            {frozenset({"a", "c"}), frozenset({"b"})}
        )

    def test_directed_chain(self):
        # 1 -> 2 -> 3
        af = ArgumentationFramework(
            arguments={"1", "2", "3"},
            attacks={("1", "2"), ("2", "3")}
        )
        grounded = compute_grounded(af)
        self.assertEqual(grounded, {"1", "3"})

        preferred = compute_preferred(af)
        self.assertEqual(preferred, [{"1", "3"}])

        stable = compute_stable(af)
        self.assertEqual(stable, [{"1", "3"}])

    def test_odd_three_cycle(self):
        # a -> b -> c -> a
        af = ArgumentationFramework(
            arguments={"a", "b", "c"},
            attacks={("a", "b"), ("b", "c"), ("c", "a")}
        )
        exts = compute_all_extensions(af)

        self.assertEqual(exts["grounded"], set())
        self.assertEqual(exts["complete"], [set()])
        self.assertEqual(exts["preferred"], [set()])
        # Stable extensions DO NOT exist on an odd 3-cycle
        self.assertEqual(exts["stable"], [])
        # Semi-stable always exists
        self.assertEqual(exts["semi_stable"], [set()])

    def test_even_four_cycle(self):
        # 1 -> 2 -> 3 -> 4 -> 1
        af = ArgumentationFramework(
            arguments={"1", "2", "3", "4"},
            attacks={("1", "2"), ("2", "3"), ("3", "4"), ("4", "1")}
        )
        exts = compute_all_extensions(af)

        self.assertEqual(exts["grounded"], set())
        self.assertEqual(
            set(map(frozenset, exts["preferred"])),
            {frozenset({"1", "3"}), frozenset({"2", "4"})}
        )
        self.assertEqual(
            set(map(frozenset, exts["stable"])),
            {frozenset({"1", "3"}), frozenset({"2", "4"})}
        )

    def test_self_attacking_argument(self):
        # a -> a, a -> b, c -> b
        af = ArgumentationFramework(
            arguments={"a", "b", "c"},
            attacks={("a", "a"), ("a", "b"), ("c", "b")}
        )
        grounded = compute_grounded(af)
        # c is unattacked -> accepted. b is attacked by accepted c -> rejected.
        # a attacks itself -> never accepted in conflict-free set.
        # Since only a attacks a, no outside conflict-free set can attack a, so no stable extension exists!
        self.assertEqual(grounded, {"c"})
        self.assertEqual(compute_preferred(af), [{"c"}])
        self.assertEqual(compute_stable(af), [])
        self.assertEqual(compute_semi_stable(af), [{"c"}])

    def test_semi_stable_distinction_from_stable(self):
        # Framework with no stable extension, but non-empty semi-stable
        # a attacks itself (a -> a). b unattacked (b).
        af = ArgumentationFramework(
            arguments={"a", "b"},
            attacks={("a", "a")}
        )
        exts = compute_all_extensions(af)
        self.assertEqual(exts["grounded"], {"b"})
        self.assertEqual(exts["preferred"], [{"b"}])
        # {b} range is {b} (does not attack a). So no stable extension!
        self.assertEqual(exts["stable"], [])
        # Semi-stable range is {b}, which is maximal among complete ({b})
        self.assertEqual(exts["semi_stable"], [{"b"}])

    def test_theoretical_inclusions(self):
        # Test hierarchy on various topologies:
        # Grounded subseteq every complete
        # Stable subseteq Semi-stable subseteq Preferred subseteq Complete
        graphs = [
            ArgumentationFramework({"a", "b", "c"}, {("a", "b"), ("b", "a"), ("b", "c")}),
            ArgumentationFramework({"1", "2", "3", "4"}, {("1", "2"), ("2", "3"), ("3", "4"), ("4", "1")}),
            ArgumentationFramework({"x", "y"}, {("x", "y")}),
            ArgumentationFramework({"p", "q", "r"}, {("p", "q"), ("q", "r"), ("r", "p")}),
        ]

        for af in graphs:
            exts = compute_all_extensions(af)
            grounded = exts["grounded"]
            complete = exts["complete"]
            preferred = exts["preferred"]
            stable = exts["stable"]
            semi_stable = exts["semi_stable"]

            # Grounded in all complete
            for c in complete:
                self.assertTrue(grounded.issubset(c))

            # Every stable is semi-stable
            for s in stable:
                self.assertIn(s, semi_stable)

            # Every semi-stable is preferred
            for ss in semi_stable:
                self.assertIn(ss, preferred)

            # Every preferred is complete
            for p in preferred:
                self.assertIn(p, complete)


if __name__ == "__main__":
    unittest.main()
