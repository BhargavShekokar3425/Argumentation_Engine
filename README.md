# Abstract Argumentation Engine & Strategic Mechanism

A rigorous computational engine and game-theoretic mechanism implementation for **Abstract Argumentation Frameworks**, **Argumentation Semantics**, and **Strategic Argumentation (Mechanism Design)**.

Developed for * Argumentation Engine**, this project combines:
- **Artificial Intelligence**: Acceptability and justification of arguments under classical Dung semantics.
- **Graph Theory**: Caminada 3-valued argument labellings, cycles, and parity-aware odd-path graph traversals.
- **Game Theory & Mechanism Design**: Grounded direct mechanisms, strategic argument hiding, and empirical verification of **Theorem 5.3** (Strategyproofness) and **Theorem 5.4** (Sufficient structural condition).

---

## Table of Contents
1. [Core Features](#core-features)
2. [Project Architecture](#project-architecture)
3. [Theoretical Overview](#theoretical-overview)
4. [Textbook Misprints Clarification](#textbook-misprints-clarification)
5. [Installation & Requirements](#installation--requirements)
6. [Quickstart & Demonstration](#quickstart--demonstration)
7. [Running the Test Suite](#running-the-test-suite)
8. [Randomized Experiments (3,000 Runs)](#randomized-experiments-3000-runs)
9. [Experimental Results Summary](#experimental-results-summary)
10. [Deliverables & Report](#deliverables--report)

---

## Core Features

### Part 1: Argumentation Engine
- **Framework Representation**: Directed attack graphs $AF = \langle A, R \rangle$ with precomputed incoming/outgoing adjacency sets and validated endpoints.
- **Fundamental Properties**:
  - Conflict-freeness check ($S \cap S^+ = \emptyset$).
  - Defense / Acceptability check ($\forall b \in attackers(a), \exists c \in S \text{ s.t. } (c, b) \in R$).
  - Characteristic function $F_{AF}(S) = \{a \in A \mid S \text{ defends } a\}$.
  - Admissibility check ($S$ is conflict-free and $S \subseteq F(S)$).
  - Complete extension check ($S$ is conflict-free and $S = F(S)$).
- **Semantics Computation**:
  - **Grounded Extension**: Unique least fixed point of $F_{AF}$ computed by Kleene iteration from $\emptyset$.
  - **Complete Extensions**: All conflict-free fixed points of $F_{AF}$.
  - **Preferred Extensions**: Inclusion-maximal admissible sets (inclusion-maximal complete extensions).
  - **Stable Extensions**: Conflict-free sets attacking every outside argument ($S^+ = A \setminus S$). Returns `[]` when none exist (e.g. odd 3-cycle).
  - **Semi-stable Extensions**: Complete extensions with inclusion-maximal range $S \cup S^+$.
- **Caminada 3-Valued Labellings**:
  - Bijective generation of $(IN, OUT, UNDEC)$ labellings from complete extensions.
  - Independent condition validation:
    1. $x \in IN \iff \forall y \in attackers(x), y \in OUT$.
    2. $x \in OUT \iff \exists y \in attackers(x), y \in IN$.
    3. $x \in UNDEC \iff (\forall y, y \notin IN) \land (\exists y, y \in UNDEC)$.
- **Acceptance Status**:
  - Classifies any argument $\alpha$ under any chosen semantics as **Skeptically accepted** ($\alpha \in \bigcap \mathcal{E}$), **Credulously accepted** ($\alpha \in \bigcup \mathcal{E}$), or **Rejected**.
  - Handles empty extension sets cleanly (e.g., stable semantics on odd cycles).

### Part 2: Strategic Argumentation
- **Grounded Direct Argumentation Mechanism**:
  - $N$ agents partition arguments: $A = \bigcup_{i=1}^N A_i$.
  - Agents submit reports $R_i \subseteq A_i$ (revealed subsets).
  - Evaluates the grounded extension of the induced subgraph $AF[\bigcup R_i]$.
  - Correctly removes incident attacks when arguments are hidden.
- **Utility Function**:
  - $u_i(R_1, \dots, R_N) = |A_i \cap g(R_1, \dots, R_N)|$ (measured against *true* owned arguments $A_i$).
- **Best Responses**:
  - Enumerates all subsets $S_i \subseteq A_i$ and returns *all* maximizing reports.
- **Theorem 5.3 (Strategyproofness Verification)**:
  - Exhaustively tests whether truthfulness $A_i$ is a best response against *every* possible profile of reports by other agents $R_{-i} \in \prod_{j \neq i} 2^{A_j}$.
  - Returns explicit counterexample witnesses on failure (agent, hidden arguments, utilities, outcomes).
- **Theorem 5.4 (Odd-Length Path Condition)**:
  - Verifies whether any agent owns arguments $\alpha, \beta$ connected by an odd-length directed path.
  - Handles cycles correctly via parity-aware BFS (tracking state `(vertex, parity)`) and simple path DFS.
  - Accounts for self-attacks ($\alpha \to \alpha$, length 1) and odd cycles.

### Part 3: Randomized Experiments & Optimization
- **3,000 Total Random Instances**:
  - 1,000 runs per attack probability $p \in \{0.15, 0.25, 0.35\}$.
  - 6 to 8 arguments partitioned randomly among 3 agents.
- **High-Performance Caching**:
  - Precomputes $G[X] = GE(AF[X])$ for all $X \subseteq A$ ($2^8 = 256$ subsets).
  - Completes 3,000 full game-theoretic evaluations in **2.5 seconds** (~1,200 instances/sec).
- **Vector Plots & Interactive Dashboard**:
  - Zero-dependency SVG generators for grouped comparison and stacked category breakdown charts.
  - Interactive HTML dashboard (`results/dashboard.html`) for browser inspection.

---

## Project Architecture

```
argumentation_engine/
├── src/
│   └── argumentation/
│       ├── __init__.py           # Package exports
│       ├── framework.py          # ArgumentationFramework class & graph operations
│       ├── defense.py            # Conflict-free, defense, characteristic function F
│       ├── semantics.py          # Grounded, Complete, Preferred, Stable, Semi-stable
│       ├── labelling.py          # Caminada 3-valued labellings (IN/OUT/UNDEC)
│       ├── acceptance.py         # Skeptical, credulous, rejected acceptance status
│       ├── mechanism.py          # Grounded direct mechanism & best responses
│       ├── strategyproof.py      # Theorem 5.3 (exact) & Theorem 5.4 (odd-path)
│       ├── graph_generator.py    # Random AF & agent partition generator
│       └── visualizer.py         # Terminal ASCII tables & formatting
├── experiments/
│   ├── run_experiments.py       # 3,000 instance benchmark suite
│   └── plot_results.py          # SVG chart & HTML dashboard generator
├── tests/
│   ├── test_framework.py        # Framework, defense & characteristic tests
│   ├── test_semantics.py        # Classical semantics & hierarchy tests
│   ├── test_labelling_acceptance.py # Labellings & acceptance tests
│   └── test_strategic.py        # Strategic manipulation, Thm 5.3 & 5.4 tests
├── examples/
│   └── textbook_examples.py     # Canonical textbook cases (5.10, 5.11, 3-cycles)
├── results/
│   ├── instances.csv            # Granular data for all 3,000 instances
│   ├── summary.csv              # Aggregated statistics by probability p
│   ├── counterexamples.json     # Manipulation witnesses & edge cases
│   ├── strategyproof_comparison.svg # Vector comparison chart
│   ├── outcomes_breakdown.svg   # Vector stacked breakdown chart
│   └── dashboard.html           # Interactive visual dashboard
├── demo.py                      # 6-step interactive/automated demonstration
├── REPORT.md                    # Comprehensive 8-12 page technical report
├── README.md                    # Project documentation (this file)
└── requirements.txt             # Project dependencies (zero external required!)
```

---

## Theoretical Overview

### Dung Semantics Hierarchy
For any finite argumentation framework $AF = \langle A, R \rangle$:
$$\text{Stable} \subseteq \text{Semi-stable} \subseteq \text{Preferred} \subseteq \text{Complete} \subseteq \text{Admissible}$$
$$\text{Grounded} \subseteq \bigcap \text{Complete}$$

- **Grounded Extension**: Always exists, always unique.
- **Preferred Extension**: Always exists (at least one).
- **Semi-stable Extension**: Always exists in finite frameworks. If stable extensions exist, semi-stable extensions coincide with stable extensions.
- **Stable Extension**: May not exist (e.g. directed 3-cycle $a \to b \to c \to a$).

### Strategic Argumentation & Direct Mechanisms
Let agents $1, \dots, N$ hold a disjoint partition $A = \bigcup_{i=1}^N A_i$.
When agents reveal subsets $R_i \subseteq A_i$, the mechanism selects the grounded extension of the induced graph:
$$g(R_1, \dots, R_N) = GE\left(AF\left[\bigcup_{i=1}^N R_i\right]\right)$$
The utility of agent $i$ is:
$$u_i(R_1, \dots, R_N) = \left|A_i \cap g(R_1, \dots, R_N)\right|$$

### Theorem 5.3 vs. Theorem 5.4
- **Theorem 5.3 (Strategyproofness)**:
  A mechanism is strategyproof if and only if for every agent $i$, truthful revelation is a weak dominant strategy:
  $$\forall i, \forall R_{-i}, \forall S_i \subseteq A_i: \quad u_i(A_i, R_{-i}) \ge u_i(S_i, R_{-i})$$
- **Theorem 5.4 (Odd-Length Path Condition)**:
  If no agent holds two arguments $\alpha, \beta$ connected by an odd-length directed attack path in the full graph, then the grounded direct mechanism is strategyproof.

> **Crucial Distinction**:
> **Theorem 5.4 is SUFFICIENT, NOT NECESSARY.**
> If the condition holds, strategyproofness is guaranteed. However, an instance can be strategyproof even when the condition fails (e.g., when protective arguments shield the agent's positions).

---

## Textbook Misprints Clarification

As noted on Page 2 of the assignment specification:
1. **Example 5.10 Utility Misprint**: In textbook Example 5.10, the utilities of agents $y$ and $z$ were swapped in the text. Under truthful reporting, $GE = \{1, 3\}$, meaning Agent Y ($A_Y = \{2\}$) has utility $0$, and Agent Z ($A_Z = \{3\}$) has utility $1$.
2. **Discussion after Example 5.11 Misprint**: In the text following Example 5.11, the argument that cancels the indirect self-defeat is referred to as $\alpha_5$. The correct protecting argument is $\alpha_6$, which attacks $\alpha_3$.

Both corrections are implemented, documented, and tested in `examples/textbook_examples.py`.

---

## Installation & Requirements

The core engine is built using **pure Python 3 (standard library only)**. It has **zero required external dependencies**!

### Requirements
- Python 3.8+ (tested on Python 3.12)
- Optional: `matplotlib` (if PNG export is desired; SVG and HTML generation are built-in without dependencies).

### Setup
Navigate to the directory:
```powershell
cd C:\Users\ASUS\Downloads\prog\Argumentation
```

---

## Quickstart & Demonstration

To execute the complete 6-step demonstration workflow:

```powershell
python demo.py
```

### Demonstration Steps Covered:
1. **Step 1**: Argumentation Framework initialization, adjacency dictionaries, and defense.
2. **Step 2**: Dung semantics computation (Grounded, Complete, Preferred, Stable, Semi-stable).
3. **Step 3**: Caminada 3-valued labellings and acceptance status reporting.
4. **Step 4**: Strategic argumentation with 3 agents (Example 5.10 manipulation: utility increases $1 \to 2$).
5. **Step 5**: Independent verification of Theorem 5.3 and Theorem 5.4 (including Example 5.11 protected defeat).
6. **Step 6**: Presentation of 3,000-instance experimental results, statistics, and counterexamples.

To run an individual step:
```powershell
python demo.py --step 4
```

---

## Running the Test Suite

The test suite covers 25 comprehensive unit and integration tests:

```powershell
$env:PYTHONPATH="src"
python -m unittest discover tests
```

Expected output:
```
.........................
----------------------------------------------------------------------
Ran 25 tests in 0.002s

OK
```

---

## Randomized Experiments (3,000 Runs)

To re-run the 3,000 randomized experiments across $p \in \{0.15, 0.25, 0.35\}$:

```powershell
$env:PYTHONPATH="src"
python experiments/run_experiments.py
```

To re-generate the vector charts and interactive dashboard:
```powershell
$env:PYTHONPATH="src"
python experiments/plot_results.py
```

Open `results/dashboard.html` in any web browser to view the interactive dashboard.

---

## Experimental Results Summary

From our 3,000 randomized runs (1,000 per probability level, 3 agents, $n \in \{6, 7, 8\}$):

| Attack Prob ($p$) | Instances | Strategyproof (Thm 5.3) | SP Fraction | Thm 5.4 Holds | Thm 5.4 Fraction | Cond Holds & Not SP (Exp. 0) | SP & Cond Fails |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0.15** | 1,000 | 592 | **59.20%** | 66 | 6.60% | **0** | 526 |
| **0.25** | 1,000 | 246 | **24.60%** | 4 | 0.40% | **0** | 242 |
| **0.35** | 1,000 | 130 | **13.00%** | 0 | 0.00% | **0** | 130 |
| **Overall** | **3,000** | **968** | **32.27%** | **70** | **2.33%** | **0** | **898** |

### Key Findings
1. **Soundness of Theorem 5.4**: `Cond Holds & Not SP` was **0 across all 3,000 instances**, verifying empirically that Theorem 5.4 is a sound sufficient condition.
2. **Sufficiency vs. Necessity**: **898 instances** were strategyproof despite Theorem 5.4 failing.
3. **Graph Density Impact**: As $p$ increases from 0.15 to 0.35, the fraction of strategyproof frameworks drops sharply from 59.2% to 13.0% due to the formation of dense attack cycles.

---

## Deliverables & Report

- **Code**: Clean, typed, modular code in `src/argumentation/`.
- **Tests**: Exhaustive test suite in `tests/`.
- **Demonstration**: Automated walkthrough script in `demo.py`.
- **Technical Report**: Full 8-12 page equivalent comprehensive report in [`REPORT.md`](REPORT.md).
- **Interactive Dashboard**: `results/dashboard.html`.
- **Raw Data**: `results/instances.csv`, `results/summary.csv`, `results/counterexamples.json`.
