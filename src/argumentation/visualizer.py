"""
Terminal Visualizer and Graph Display Utilities.

Provides ASCII/text-based visualization of Argumentation Frameworks,
extensions, Caminada labellings, and strategic utility payoff tables.
"""

from typing import Dict, List, Set, Any
from .framework import ArgumentationFramework
from .labelling import Labelling


def format_set(s: Set[Any]) -> str:
    """Format a set cleanly as {a, b, c} or empty set."""
    if not s:
        return "{}"
    return "{" + ", ".join(sorted([str(x) for x in s])) + "}"


def format_extensions_list(exts: List[Set[Any]]) -> str:
    """Format a list of sets cleanly."""
    if not exts:
        return "[] (None exist)"
    return "[" + ", ".join(format_set(e) for e in exts) + "]"


def render_framework_summary(af: ArgumentationFramework) -> str:
    """Render a clean text summary of an Argumentation Framework."""
    lines = []
    lines.append(f"Arguments ({len(af.arguments)}): {format_set(af.arguments)}")
    lines.append(f"Attacks   ({len(af.attacks)}):")
    if not af.attacks:
        lines.append("  (No attacks - completely unattacked graph)")
    else:
        for u, v in sorted(af.attacks, key=lambda x: (str(x[0]), str(x[1]))):
            lines.append(f"  {u}  --->  {v}")
    lines.append("Adjacency (Attackers of each argument):")
    for a in sorted(af.arguments, key=lambda x: str(x)):
        attackers = af.attackers[a]
        lines.append(f"  {a}: attacked by {format_set(attackers)}")
    return "\n".join(lines)


def render_labelling_table(labellings: List[Labelling]) -> str:
    """Render Caminada labellings in a clean table format."""
    lines = []
    lines.append(f"{'#':<4} | {'IN (Accepted)':<25} | {'OUT (Defeated)':<25} | {'UNDEC (Undecided)':<25}")
    lines.append("-" * 85)
    for idx, lab in enumerate(labellings, 1):
        in_str = format_set(lab.in_set)
        out_str = format_set(lab.out_set)
        undec_str = format_set(lab.undec_set)
        lines.append(f"{idx:<4} | {in_str:<25} | {out_str:<25} | {undec_str:<25}")
    return "\n".join(lines)


def render_acceptance_table(statuses: List[Dict[str, Any]]) -> str:
    """Render acceptance statuses for multiple arguments."""
    lines = []
    lines.append(f"{'Argument':<10} | {'Semantics':<12} | {'Status':<16} | {'Skeptical?':<12} | {'Credulous?':<12}")
    lines.append("-" * 72)
    for s in statuses:
        lines.append(
            f"{str(s['argument']):<10} | {s['semantics']:<12} | {s['status']:<16} | {str(s['is_skeptical']):<12} | {str(s['is_credulous']):<12}"
        )
    return "\n".join(lines)


def render_strategic_utility_comparison(
    partition: Dict[str, Set[Any]],
    truthful_outcome: Set[Any],
    manipulated_reports: Dict[str, Set[Any]],
    manipulated_outcome: Set[Any]
) -> str:
    """Render a strategic comparison of utilities under truthful vs manipulated reports."""
    lines = []
    lines.append(f"{'Agent':<8} | {'Owned Args':<18} | {'Truthful Rep':<16} | {'Truthful Util':<14} | {'Deviated Rep':<16} | {'Deviated Util':<14}")
    lines.append("-" * 92)

    for agent, owned in partition.items():
        t_rep = format_set(owned)
        t_util = len(owned & truthful_outcome)

        m_rep = format_set(manipulated_reports.get(agent, owned))
        m_util = len(owned & manipulated_outcome)

        delta = m_util - t_util
        delta_str = f" (+{delta} GAIN!)" if delta > 0 else (" (0)" if delta == 0 else f" ({delta})")

        lines.append(
            f"{agent:<8} | {format_set(owned):<18} | {t_rep:<16} | {t_util:<14} | {m_rep:<16} | {str(m_util) + delta_str:<14}"
        )

    lines.append("-" * 92)
    lines.append(f"Truthful Grounded Extension:   {format_set(truthful_outcome)}")
    lines.append(f"Manipulated Grounded Extension: {format_set(manipulated_outcome)}")
    return "\n".join(lines)
