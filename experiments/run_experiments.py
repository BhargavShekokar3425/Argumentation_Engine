"""
Run Randomized Experiments for Strategic Argumentation.

Generates 3,000 random instances across:
- p in {0.15, 0.25, 0.35} (1,000 instances per probability)
- n in {6, 7, 8} arguments
- 3 agents (random partition)
- Both Theorem 5.3 (exact strategyproofness) and Theorem 5.4 (odd-path condition) evaluated.

Saves:
- results/instances.csv
- results/summary.csv
- results/counterexamples.json
"""

import os
import sys
import csv
import json
import time
import random
from typing import Dict, List, Any

# Ensure src is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from argumentation.framework import ArgumentationFramework
from argumentation.strategyproof import (
    check_theorem_5_3,
    check_theorem_5_4,
    precompute_grounded_cache,
)
from argumentation.graph_generator import generate_random_af, random_agent_partition


def run_experiment_suite(
    probabilities: List[float] = [0.15, 0.25, 0.35],
    instances_per_p: int = 1000,
    arg_sizes: List[int] = [6, 7, 8],
    base_seed: int = 42,
    output_dir: str = "results"
) -> Dict[str, Any]:
    """Execute the full experimental suite."""
    os.makedirs(output_dir, exist_ok=True)
    csv_instances_path = os.path.join(output_dir, "instances.csv")
    csv_summary_path = os.path.join(output_dir, "summary.csv")
    json_counterexamples_path = os.path.join(output_dir, "counterexamples.json")

    start_time = time.time()
    print(f"Starting experiments: {len(probabilities)} probabilities x {instances_per_p} instances = {len(probabilities)*instances_per_p} total.")

    instances_data = []
    summary_by_p = {p: {
        "p": p,
        "total": 0,
        "sp_count": 0,
        "thm54_holds_count": 0,
        "cond_holds_but_not_sp": 0,  # Case 2: Should be 0
        "sp_despite_cond_fails": 0,  # Case 3: Sufficient not necessary
        "not_sp_and_cond_fails": 0,
    } for p in probabilities}

    counterexamples_records = {
        "manipulation_witnesses": [],
        "sp_despite_cond_fails_examples": [],
        "cond_holds_but_not_sp_anomalies": []
    }

    instance_counter = 0

    for p in probabilities:
        print(f"--> Running p = {p} ({instances_per_p} instances)...")
        p_start = time.time()

        for idx in range(instances_per_p):
            instance_counter += 1
            seed = base_seed + instance_counter

            # Distribute argument counts across 6, 7, 8
            n = arg_sizes[idx % len(arg_sizes)]

            # Generate random framework and agent partition
            af = generate_random_af(
                num_arguments=n,
                attack_probability=p,
                allow_self_attacks=True,
                seed=seed,
                arg_prefix="a"
            )
            partition = random_agent_partition(
                arguments=af.arguments,
                num_agents=3,
                ensure_non_empty=True,
                seed=seed + 1000000
            )

            # Precompute cache for grounded extension lookups
            cache = precompute_grounded_cache(af)

            # Evaluate Theorem 5.3 (Exact Strategyproofness)
            is_sp, ce_53 = check_theorem_5_3(af, partition, cache=cache)

            # Evaluate Theorem 5.4 (Structural Condition: Parity Walk)
            cond_54_holds, witness_54 = check_theorem_5_4(af, partition, use_simple_path=False)

            # Evaluate Theorem 5.4 using Simple Path as well
            cond_54_simple, witness_54_simple = check_theorem_5_4(af, partition, use_simple_path=True)

            # Classify instance
            if cond_54_holds and not is_sp:
                category = "NotSP_and_CondHolds"
                summary_by_p[p]["cond_holds_but_not_sp"] += 1
                counterexamples_records["cond_holds_but_not_sp_anomalies"].append({
                    "instance_id": instance_counter,
                    "p": p,
                    "n": n,
                    "seed": seed,
                    "framework": af.to_dict(),
                    "partition": {k: list(v) for k, v in partition.items()},
                    "counterexample_53": ce_53,
                })
            elif is_sp and not cond_54_holds:
                category = "SP_and_CondFails"
                summary_by_p[p]["sp_despite_cond_fails"] += 1
                if len(counterexamples_records["sp_despite_cond_fails_examples"]) < 20:
                    counterexamples_records["sp_despite_cond_fails_examples"].append({
                        "instance_id": instance_counter,
                        "p": p,
                        "n": n,
                        "seed": seed,
                        "framework": af.to_dict(),
                        "partition": {k: sorted(list(v)) for k, v in partition.items()},
                        "odd_path_witness": witness_54,
                    })
            elif is_sp and cond_54_holds:
                category = "SP_and_CondHolds"
            else:
                category = "NotSP_and_CondFails"
                summary_by_p[p]["not_sp_and_cond_fails"] += 1
                if len(counterexamples_records["manipulation_witnesses"]) < 20:
                    counterexamples_records["manipulation_witnesses"].append({
                        "instance_id": instance_counter,
                        "p": p,
                        "n": n,
                        "seed": seed,
                        "framework": af.to_dict(),
                        "partition": {k: sorted(list(v)) for k, v in partition.items()},
                        "counterexample": ce_53,
                        "odd_path_witness": witness_54,
                    })

            if is_sp:
                summary_by_p[p]["sp_count"] += 1
            if cond_54_holds:
                summary_by_p[p]["thm54_holds_count"] += 1
            summary_by_p[p]["total"] += 1

            has_self_attack = any(u == v for u, v in af.attacks)

            instances_data.append({
                "instance_id": instance_counter,
                "p": p,
                "num_arguments": n,
                "num_attacks": len(af.attacks),
                "has_self_attacks": has_self_attack,
                "is_strategyproof": is_sp,
                "thm54_condition_holds": cond_54_holds,
                "thm54_simple_path_holds": cond_54_simple,
                "category": category,
                "seed": seed,
            })

        p_elapsed = time.time() - p_start
        print(f"    Completed p = {p} in {p_elapsed:.2f}s.")

    total_elapsed = time.time() - start_time
    print(f"All 3,000 instances completed in {total_elapsed:.2f}s ({3000/total_elapsed:.1f} instances/s).")

    # Write instances.csv
    print(f"Writing {csv_instances_path}...")
    with open(csv_instances_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "instance_id", "p", "num_arguments", "num_attacks", "has_self_attacks",
            "is_strategyproof", "thm54_condition_holds", "thm54_simple_path_holds",
            "category", "seed"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(instances_data)

    # Compute summary percentages and write summary.csv
    summary_rows = []
    print("\n================== EXPERIMENTAL RESULTS SUMMARY ==================")
    print(f"{'p':<6} | {'Total':<6} | {'SP Count':<8} | {'SP Fraction':<11} | {'Thm 5.4 Count':<13} | {'Thm 5.4 Frac':<12} | {'CondHolds & NotSP':<17} | {'SP & CondFails':<14}")
    print("-" * 105)

    for p in probabilities:
        stats = summary_by_p[p]
        tot = stats["total"]
        sp_frac = stats["sp_count"] / tot
        thm54_frac = stats["thm54_holds_count"] / tot

        row = {
            "p": p,
            "total_instances": tot,
            "strategyproof_count": stats["sp_count"],
            "strategyproof_fraction": round(sp_frac, 4),
            "thm54_holds_count": stats["thm54_holds_count"],
            "thm54_holds_fraction": round(thm54_frac, 4),
            "cond_holds_but_not_sp": stats["cond_holds_but_not_sp"],
            "sp_despite_cond_fails": stats["sp_despite_cond_fails"],
            "not_sp_and_cond_fails": stats["not_sp_and_cond_fails"],
        }
        summary_rows.append(row)

        print(f"{p:<6} | {tot:<6} | {stats['sp_count']:<8} | {sp_frac:<11.4f} | {stats['thm54_holds_count']:<13} | {thm54_frac:<12.4f} | {stats['cond_holds_but_not_sp']:<17} | {stats['sp_despite_cond_fails']:<14}")

    print("=" * 105)

    with open(csv_summary_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "p", "total_instances", "strategyproof_count", "strategyproof_fraction",
            "thm54_holds_count", "thm54_holds_fraction",
            "cond_holds_but_not_sp", "sp_despite_cond_fails", "not_sp_and_cond_fails"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    # Write counterexamples.json
    with open(json_counterexamples_path, "w", encoding="utf-8") as f:
        json.dump(counterexamples_records, f, indent=2)

    return {
        "summary": summary_rows,
        "elapsed_time": total_elapsed,
        "anomalies_count": sum(r["cond_holds_but_not_sp"] for r in summary_rows)
    }


if __name__ == "__main__":
    run_experiment_suite()
