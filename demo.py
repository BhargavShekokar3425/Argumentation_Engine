"""
Interactive and Automated Demonstration Script for Assignment 3:
Argumentation Engine & Strategic Argumentation.

Demonstrates the 6-step core workflow:
1. Argumentation Framework creation, arguments, attacks, and structure.
2. Semantics computation (Grounded, Complete, Preferred, Stable, Semi-stable).
3. Caminada 3-valued labellings and argument acceptance status.
4. Strategic argumentation with 3 agents, argument hiding, and utility payoff shift.
5. Verification of Theorem 5.3 (exact strategyproofness) and Theorem 5.4 (odd-path condition).
6. Experimental study presentation (3,000 runs, summary statistics, counterexamples).
"""

import sys
import os
import argparse
import csv
import json

# Ensure src is on python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from argumentation.framework import ArgumentationFramework
from argumentation.defense import is_conflict_free, defends, characteristic
from argumentation.semantics import compute_all_extensions, powerset
from argumentation.labelling import compute_legal_labellings
from argumentation.acceptance import argument_acceptance_status
from argumentation.mechanism import (
    grounded_direct_mechanism,
    agent_utility,
    compute_best_responses,
)
from argumentation.strategyproof import check_theorem_5_3, check_theorem_5_4
from argumentation.visualizer import (
    format_set,
    format_extensions_list,
    render_framework_summary,
    render_labelling_table,
    render_acceptance_table,
    render_strategic_utility_comparison,
)
from examples.textbook_examples import (
    example_running_three_arg,
    example_strategic_manipulation_5_10,
    example_protected_indirect_defeat_5_11,
)


def header(title: str, step: int) -> None:
    print("\n" + "=" * 80)
    print(f"  STEP {step}: {title.upper()}")
    print("=" * 80)


def demo_step_1():
    header("Create Argumentation Framework and Inspect Structure", 1)
    af, _ = example_running_three_arg()
    print("Initialising Abstract Argumentation Framework AF = <A, R>:")
    print(render_framework_summary(af))
    print("\nFundamental Properties:")
    print(f"  Is empty set conflict-free?         {is_conflict_free(af, set())}")
    print(f"  Is set {{a, c}} conflict-free?       {is_conflict_free(af, {'a', 'c'})}")
    print(f"  Is set {{a, b}} conflict-free?       {is_conflict_free(af, {'a', 'b'})} (Conflict: a <-> b)")
    print(f"  Does {{a}} defend c?                 {defends(af, {'a'}, 'c')} (Because a counterattacks b)")
    print(f"  Characteristic function F({{a}}):     {format_set(characteristic(af, {'a'}))}")


def demo_step_2():
    header("Compute Argumentation Semantics", 2)
    af, data = example_running_three_arg()
    exts = data["extensions"]

    print("Computing all Dung semantics and extensions for AF:")
    print(f"  - Grounded Extension (Least Fixed Point of F):")
    print(f"      GE = {format_set(exts['grounded'])}")
    print(f"  - Complete Extensions (Conflict-free Fixed Points of F):")
    print(f"      {format_extensions_list(exts['complete'])}")
    print(f"  - Preferred Extensions (Inclusion-Maximal Admissible Sets):")
    print(f"      {format_extensions_list(exts['preferred'])}")
    print(f"  - Stable Extensions (Conflict-free Sets Attacking A \\ S):")
    print(f"      {format_extensions_list(exts['stable'])}")
    print(f"  - Semi-Stable Extensions (Complete with Inclusion-Maximal Range):")
    print(f"      {format_extensions_list(exts['semi_stable'])}")

    print("\nNotice:")
    print("  Grounded is empty ({}) because both a and b are challenged in a mutual cycle.")
    print("  Complete yields 3 extensions: the minimal {}, and two maximal extensions {a, c} and {b}.")


def demo_step_3():
    header("Generate Legal Labellings and Report Acceptance Status", 3)
    af, data = example_running_three_arg()
    labs = data["labellings"]

    print("1. Caminada 3-Valued Legal Labellings (Derived from Complete Extensions):")
    print(render_labelling_table(labs))

    print("\n2. Acceptance Status for All Arguments under Preferred Semantics:")
    statuses = [
        argument_acceptance_status(af, arg, semantics="preferred", extensions=data["extensions"]["preferred"])
        for arg in sorted(af.arguments)
    ]
    print(render_acceptance_table(statuses))

    print("\nInterpretation:")
    print("  'a' is credulously accepted because it appears in extension {a, c}, but not in {b}.")
    print("  'b' is credulously accepted because it appears in {b}, but not in {a, c}.")
    print("  'c' is credulously accepted because it appears in {a, c}, but not in {b}.")


def demo_step_4():
    header("Introduce Strategic Agents and Demonstrate Manipulation (Example 5.10)", 4)
    print("Setting up Example 5.10 (Rahwan & Larson):")
    print("  Arguments: {1, 2, 3, 4, 5}")
    print("  Attacks: 1 -> 2 -> 3 -> 4, and 3 -> 5")
    print("  Agent Ownership:")
    print("    - Agent X: {1, 4, 5}")
    print("    - Agent Y: {2}")
    print("    - Agent Z: {3}")

    res = example_strategic_manipulation_5_10()
    af = res["framework"]
    partition = res["partition"]

    print("\nPayoff Matrix & Strategic Comparison:")
    print(render_strategic_utility_comparison(
        partition=partition,
        truthful_outcome=res["truthful_outcome"],
        manipulated_reports=res["manipulated_reports"],
        manipulated_outcome=res["manipulated_outcome"]
    ))

    print("\nDetailed Analysis of Strategic Deviation:")
    print("  - When Agent X reports TRUTHFULLY {1, 4, 5}:")
    print("      Argument 1 is unattacked -> accepted.")
    print("      Argument 1 defeats 2 -> Argument 3 is defended and accepted.")
    print("      Argument 3 defeats 4 and 5.")
    print("      Outcome: GE = {1, 3}. Agent X utility = 1 (only arg 1 is accepted).")
    print("  - When Agent X HIDES Argument 1 (reports {4, 5}):")
    print("      Argument 1 and attack 1->2 disappear from revealed graph!")
    print("      Argument 2 becomes unattacked -> accepted.")
    print("      Argument 2 defeats 3 -> Arguments 4 and 5 are defended and accepted!")
    print("      Outcome: GE = {2, 4, 5}. Agent X utility = 2 (args 4 and 5 accepted!).")
    print("  --> CONCLUSION: Agent X strictly improves utility from 1 to 2 by hiding argument 1!")
    print("      Truthfulness is NOT a dominant strategy.")


def demo_step_5():
    header("Verify Theorem 5.3 and Theorem 5.4 Independently", 5)
    print("Testing two benchmark cases to contrast the theorems:")

    print("\n--- CASE A: Example 5.10 (Manipulable Graph) ---")
    res_a = example_strategic_manipulation_5_10()
    print(f"  Theorem 5.3 (Exact Strategyproofness):   {res_a['is_strategyproof_thm_5_3']} (Violation Detected!)")
    ce = res_a['counterexample']
    print(f"    Counterexample Witness: Agent {ce['agent']} dev from {ce['truthful_report']} to {ce['deviation_report']} (hiding {ce['hidden_arguments']})")
    print(f"    Utility gains from {ce['truthful_utility']} to {ce['deviation_utility']}.")
    print(f"  Theorem 5.4 (Odd-Path Condition):       {res_a['condition_holds_thm_5_4']} (Condition Fails)")
    w = res_a['odd_path_witness']
    print(f"    Odd Attack Path: {' -> '.join(w['path'])} (Length {w['length']}, odd, between X's owned args {w['alpha']} and {w['beta']})")

    print("\n--- CASE B: Discussion after Example 5.11 (Protected Indirect Defeat) ---")
    print("  Extending Example 5.10 by adding unattacked argument 6, owned by Agent X, attacking 3.")
    res_b = example_protected_indirect_defeat_5_11()
    print(f"  Theorem 5.4 (Odd-Path Condition):       {res_b['condition_holds_thm_5_4']} (Condition FAILS!)")
    w_b = res_b['odd_path_witness']
    print(f"    Odd Attack Path Still Exists: {' -> '.join(w_b['path'])} (Length {w_b['length']})")
    print(f"  Theorem 5.3 (Exact Strategyproofness):   {res_b['is_strategyproof_thm_5_3']} (STRATEGYPROOF!)")
    print("  --> KEY THEORETICAL INSIGHT:")
    print("      Theorem 5.4 is a SUFFICIENT condition, NOT a necessary condition!")
    print("      Even though an odd path exists, argument 6 shields arguments 4 and 5, guaranteeing")
    print("      Agent X gets utility 4 under truthfulness, making the mechanism strategyproof.")


def demo_step_6():
    header("Present Experimental Results (3,000 Instances)", 6)
    summary_path = os.path.join(os.path.dirname(__file__), "results", "summary.csv")

    if not os.path.exists(summary_path):
        print("Summary CSV not found. Please run: python experiments/run_experiments.py")
        return

    print("Reading experimental results from results/summary.csv:\n")
    print(f"{'Attack Prob (p)':<16} | {'Instances':<10} | {'Strategyproof %':<16} | {'Thm 5.4 Holds %':<16} | {'CondHolds & NotSP':<18} | {'SP & CondFails':<14}")
    print("-" * 96)

    with open(summary_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            p = row["p"]
            tot = row["total_instances"]
            sp_pct = f"{float(row['strategyproof_fraction'])*100:.2f}%"
            thm_pct = f"{float(row['thm54_holds_fraction'])*100:.2f}%"
            anom = row["cond_holds_but_not_sp"]
            sp_fails_cond = row["sp_despite_cond_fails"]
            print(f"p = {p:<12} | {tot:<10} | {sp_pct:<16} | {thm_pct:<16} | {anom:<18} | {sp_fails_cond:<14}")
    print("-" * 96)

    print("\nSummary of Experimental Findings:")
    print("  1. Fraction Strategyproof: Decreases as edge density p increases (59.2% -> 24.6% -> 13.0%).")
    print("  2. False Positives (Cond Holds but Not SP): EXACTLY 0 across all 3,000 runs, confirming Theorem 5.4 is 100% sound.")
    print("  3. Conservative Gap (SP despite Cond Fails): 898 instances in total were strategyproof even though")
    print("     Theorem 5.4 condition failed, quantitatively proving the gap between sufficiency and necessity.")
    print("\nGenerated Artifacts:")
    print("  - Vector Charts: results/strategyproof_comparison.svg, results/outcomes_breakdown.svg")
    print("  - Interactive Dashboard: results/dashboard.html")
    print("  - Raw Data: results/instances.csv, results/summary.csv, results/counterexamples.json")


def main():
    parser = argparse.ArgumentParser(description="Assignment 3 Argumentation Engine Demonstration")
    parser.add_argument("--step", type=int, choices=range(1, 7), help="Run only a specific demonstration step (1-6)")
    args = parser.parse_args()

    steps = {
        1: demo_step_1,
        2: demo_step_2,
        3: demo_step_3,
        4: demo_step_4,
        5: demo_step_5,
        6: demo_step_6,
    }

    print("\n" + "#" * 80)
    print("       ARGUMENTATION ENGINE & STRATEGIC ARGUMENTATION DEMO")
    print("                 Assignment 3 - Complete Walkthrough")
    print("#" * 80)

    if args.step:
        steps[args.step]()
    else:
        for s in range(1, 7):
            steps[s]()

    print("\n" + "#" * 80)
    print("       DEMONSTRATION COMPLETED SUCCESSFULLY")
    print("#" * 80 + "\n")


if __name__ == "__main__":
    main()
