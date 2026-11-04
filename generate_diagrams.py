"""
Generate high-resolution, publication-grade SVG diagrams for Assignment 3:
1. system_architecture.svg
2. semantics_labelling_example.svg
3. example_5_10_manipulation.svg
4. example_5_11_protected_defeat.svg
5. parity_bfs_state_graph.svg
"""

import os
import xml.etree.ElementTree as ET

def write_and_verify(filepath, svg_content):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)
    # Validate with strict XML parser
    ET.parse(filepath)
    print(f"Generated & validated: {filepath}")


def generate_system_architecture(output_path):
    svg = r"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 560" width="950" height="560" style="background:#ffffff; font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.08"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#475569"/>
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb"/>
    </marker>
  </defs>

  <!-- Title -->
  <text x="475" y="32" text-anchor="middle" font-size="20" font-weight="700" fill="#0f172a">Argumentation Engine &amp; Strategic Mechanism Architecture</text>
  <text x="475" y="52" text-anchor="middle" font-size="12" fill="#64748b">End-to-End Computational Pipeline: Formal Semantics to Game-Theoretic Verification</text>

  <!-- LAYER 1: Core Framework -->
  <rect x="40" y="80" width="260" height="440" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="40" y="80" width="260" height="38" rx="8" fill="#e2e8f0"/>
  <text x="170" y="104" text-anchor="middle" font-size="13" font-weight="700" fill="#1e293b">1. ARGUMENTATION CORE</text>

  <rect x="55" y="130" width="230" height="55" rx="6" fill="#ffffff" stroke="#94a3b8"/>
  <text x="170" y="152" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">Framework AF = &lt;A, R&gt;</text>
  <text x="170" y="170" text-anchor="middle" font-size="10.5" fill="#64748b">Adjacency attackers / targets</text>

  <rect x="55" y="195" width="230" height="55" rx="6" fill="#ffffff" stroke="#94a3b8"/>
  <text x="170" y="217" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">Conflict-Freeness Check</text>
  <text x="170" y="235" text-anchor="middle" font-size="10.5" fill="#64748b">S ∩ S+ = ∅ (Internal attacks)</text>

  <rect x="55" y="260" width="230" height="55" rx="6" fill="#ffffff" stroke="#94a3b8"/>
  <text x="170" y="282" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">Defense (Acceptability)</text>
  <text x="170" y="300" text-anchor="middle" font-size="10.5" fill="#64748b">attackers[a] ⊆ S+</text>

  <rect x="55" y="325" width="230" height="55" rx="6" fill="#ffffff" stroke="#94a3b8"/>
  <text x="170" y="347" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">Characteristic Function F(S)</text>
  <text x="170" y="365" text-anchor="middle" font-size="10.5" fill="#64748b">F(S) = {a | S defends a}</text>

  <rect x="55" y="390" width="230" height="55" rx="6" fill="#ffffff" stroke="#94a3b8"/>
  <text x="170" y="412" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">Admissibility &amp; Complete</text>
  <text x="170" y="430" text-anchor="middle" font-size="10.5" fill="#64748b">S ⊆ F(S) and S = F(S)</text>

  <rect x="55" y="455" width="230" height="50" rx="6" fill="#ffffff" stroke="#94a3b8"/>
  <text x="170" y="476" text-anchor="middle" font-size="11.5" font-weight="600" fill="#0f172a">Erdös-Rényi Generator</text>
  <text x="170" y="492" text-anchor="middle" font-size="10" fill="#64748b">Random AF(n, p) + Seeded</text>

  <!-- Connect 1 -> 2 -->
  <line x1="300" y1="300" x2="340" y2="300" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow-blue)"/>

  <!-- LAYER 2: Semantics & Labelling -->
  <rect x="345" y="80" width="260" height="440" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="345" y="80" width="260" height="38" rx="8" fill="#e2e8f0"/>
  <text x="475" y="104" text-anchor="middle" font-size="13" font-weight="700" fill="#1e293b">2. DUNG SEMANTICS &amp; LABELS</text>

  <rect x="360" y="130" width="230" height="60" rx="6" fill="#ffffff" stroke="#3b82f6"/>
  <text x="475" y="152" text-anchor="middle" font-size="12" font-weight="600" fill="#1d4ed8">Grounded Extension</text>
  <text x="475" y="170" text-anchor="middle" font-size="10.5" fill="#64748b">Kleene Least Fixed Point: S_0 = ∅</text>
  <text x="475" y="183" text-anchor="middle" font-size="9.5" fill="#2563eb">Always unique &amp; polynomial</text>

  <rect x="360" y="200" width="230" height="50" rx="6" fill="#ffffff" stroke="#94a3b8"/>
  <text x="475" y="222" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">Complete Extensions</text>
  <text x="475" y="238" text-anchor="middle" font-size="10.5" fill="#64748b">All fixed points: S = F(S)</text>

  <rect x="360" y="260" width="230" height="50" rx="6" fill="#ffffff" stroke="#94a3b8"/>
  <text x="475" y="282" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">Preferred Extensions</text>
  <text x="475" y="298" text-anchor="middle" font-size="10.5" fill="#64748b">Inclusion-maximal admissible sets</text>

  <rect x="360" y="320" width="230" height="50" rx="6" fill="#ffffff" stroke="#94a3b8"/>
  <text x="475" y="342" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">Stable &amp; Semi-Stable</text>
  <text x="475" y="358" text-anchor="middle" font-size="10.5" fill="#64748b">S+ = A \ S / Maximal range</text>

  <rect x="360" y="380" width="230" height="65" rx="6" fill="#ffffff" stroke="#10b981"/>
  <text x="475" y="402" text-anchor="middle" font-size="12" font-weight="600" fill="#047857">Caminada 3-Valued Labels</text>
  <text x="475" y="420" text-anchor="middle" font-size="10.5" fill="#64748b">IN = E, OUT = E+, UNDEC</text>
  <text x="475" y="435" text-anchor="middle" font-size="9.5" fill="#059669">Bijective mapping &amp; verification</text>

  <rect x="360" y="455" width="230" height="50" rx="6" fill="#ffffff" stroke="#94a3b8"/>
  <text x="475" y="476" text-anchor="middle" font-size="11.5" font-weight="600" fill="#0f172a">Acceptance Status</text>
  <text x="475" y="492" text-anchor="middle" font-size="10" fill="#64748b">Skeptical ∩ / Credulous ∪ / Rejected</text>

  <!-- Connect 2 -> 3 -->
  <line x1="605" y1="300" x2="645" y2="300" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow-blue)"/>

  <!-- LAYER 3: Strategic Mechanism & Verification -->
  <rect x="650" y="80" width="260" height="440" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="650" y="80" width="260" height="38" rx="8" fill="#e2e8f0"/>
  <text x="780" y="104" text-anchor="middle" font-size="13" font-weight="700" fill="#1e293b">3. STRATEGIC MECHANISM</text>

  <rect x="665" y="130" width="230" height="60" rx="6" fill="#ffffff" stroke="#94a3b8"/>
  <text x="780" y="152" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">Agent Partition &amp; Reports</text>
  <text x="780" y="170" text-anchor="middle" font-size="10.5" fill="#64748b">A = A_1 ∪ A_2 ∪ A_3; R_i ⊆ A_i</text>
  <text x="780" y="183" text-anchor="middle" font-size="9.5" fill="#64748b">Incident attacks delete on hide</text>

  <rect x="665" y="200" width="230" height="60" rx="6" fill="#ffffff" stroke="#3b82f6"/>
  <text x="780" y="222" text-anchor="middle" font-size="12" font-weight="600" fill="#1d4ed8">Grounded Direct Mechanism</text>
  <text x="780" y="240" text-anchor="middle" font-size="10.5" fill="#64748b">g(R) = GE(AF[∪ R_i])</text>
  <text x="780" y="253" text-anchor="middle" font-size="9.5" fill="#2563eb">Utility: u_i = |A_i ∩ g(R)|</text>

  <rect x="665" y="270" width="230" height="60" rx="6" fill="#ffffff" stroke="#ef4444"/>
  <text x="780" y="292" text-anchor="middle" font-size="12" font-weight="600" fill="#b91c1c">Theorem 5.3 Verifier</text>
  <text x="780" y="310" text-anchor="middle" font-size="10.5" fill="#64748b">Dominant-Strategy IC Check</text>
  <text x="780" y="323" text-anchor="middle" font-size="9.5" fill="#ef4444">Outputs manipulation witnesses</text>

  <rect x="665" y="340" width="230" height="60" rx="6" fill="#ffffff" stroke="#10b981"/>
  <text x="780" y="362" text-anchor="middle" font-size="12" font-weight="600" fill="#047857">Theorem 5.4 Verifier</text>
  <text x="780" y="380" text-anchor="middle" font-size="10.5" fill="#64748b">2-State Parity BFS on G × Z_2</text>
  <text x="780" y="393" text-anchor="middle" font-size="9.5" fill="#059669">Odd-path indirect self-defeat</text>

  <rect x="665" y="410" width="230" height="45" rx="6" fill="#ffffff" stroke="#8b5cf6"/>
  <text x="780" y="430" text-anchor="middle" font-size="11.5" font-weight="600" fill="#6d28d9">Powerset Caching Opt</text>
  <text x="780" y="446" text-anchor="middle" font-size="9.5" fill="#64748b">Precomputes 256 subsets in 1ms</text>

  <rect x="665" y="465" width="230" height="45" rx="6" fill="#ffffff" stroke="#94a3b8"/>
  <text x="780" y="485" text-anchor="middle" font-size="11.5" font-weight="600" fill="#0f172a">Experimental Benchmark</text>
  <text x="780" y="501" text-anchor="middle" font-size="9.5" fill="#64748b">3,000 runs (p=0.15, 0.25, 0.35)</text>

  <!-- Bottom Legend Banner -->
  <text x="475" y="545" text-anchor="middle" font-size="11" fill="#94a3b8">Autonomous Systems • Assignment 3: Argumentation Engine • Pure Python 3 • Zero External Dependencies</text>
</svg>"""
    write_and_verify(output_path, svg)


def generate_semantics_labelling(output_path):
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 480" width="900" height="480" style="background:#ffffff; font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;">
  <defs>
    <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#ef4444"/>
    </marker>
    <filter id="card-sh" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.08"/>
    </filter>
  </defs>

  <text x="450" y="32" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">Argumentation Semantics &amp; Caminada Labellings (3-Argument Benchmark)</text>
  <text x="450" y="50" text-anchor="middle" font-size="12" fill="#64748b">Topology: a and b attack each other; b attacks c</text>

  <!-- Left: Graph Diagram -->
  <rect x="40" y="80" width="380" height="360" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" filter="url(#card-sh)"/>
  <text x="230" y="108" text-anchor="middle" font-size="14" font-weight="700" fill="#1e293b">Directed Attack Graph AF = &lt;A, R&gt;</text>

  <!-- Argument a -->
  <circle cx="120" cy="220" r="32" fill="#dbeafe" stroke="#2563eb" stroke-width="2.5"/>
  <text x="120" y="226" text-anchor="middle" font-size="18" font-weight="700" fill="#1e3a8a">a</text>
  <text x="120" y="270" text-anchor="middle" font-size="11" fill="#64748b">Attacks b</text>
  <text x="120" y="284" text-anchor="middle" font-size="11" fill="#64748b">Defends c</text>

  <!-- Argument b -->
  <circle cx="260" cy="220" r="32" fill="#fef3c7" stroke="#d97706" stroke-width="2.5"/>
  <text x="260" y="226" text-anchor="middle" font-size="18" font-weight="700" fill="#92400e">b</text>
  <text x="260" y="270" text-anchor="middle" font-size="11" fill="#64748b">Attacks a, c</text>
  <text x="260" y="284" text-anchor="middle" font-size="11" fill="#64748b">Defends b</text>

  <!-- Argument c -->
  <circle cx="370" cy="220" r="28" fill="#dcfce7" stroke="#10b981" stroke-width="2.5"/>
  <text x="370" y="226" text-anchor="middle" font-size="18" font-weight="700" fill="#065f46">c</text>
  <text x="370" y="270" text-anchor="middle" font-size="11" fill="#64748b">Attacked by b</text>
  <text x="370" y="284" text-anchor="middle" font-size="11" fill="#64748b">Defended by a</text>

  <!-- Attacks: a -> b (curved top), b -> a (curved bot), b -> c (straight) -->
  <path d="M 148 205 Q 190 170 230 205" fill="none" stroke="#ef4444" stroke-width="2" marker-end="url(#arr)"/>
  <path d="M 232 235 Q 190 270 152 235" fill="none" stroke="#ef4444" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="292" y1="220" x2="338" y2="220" stroke="#ef4444" stroke-width="2" marker-end="url(#arr)"/>

  <text x="190" y="175" text-anchor="middle" font-size="10.5" font-weight="600" fill="#ef4444">(a, b)</text>
  <text x="190" y="272" text-anchor="middle" font-size="10.5" font-weight="600" fill="#ef4444">(b, a)</text>
  <text x="315" y="210" text-anchor="middle" font-size="10.5" font-weight="600" fill="#ef4444">(b, c)</text>

  <!-- Key Insight Box -->
  <rect x="55" y="340" width="350" height="85" rx="6" fill="#eff6ff" stroke="#bfdbfe"/>
  <text x="65" y="360" font-size="11.5" font-weight="700" fill="#1e40af">Characteristic Function Behavior:</text>
  <text x="65" y="378" font-size="11" fill="#1e3a8a">• F(∅) = ∅ (both a and b are challenged)</text>
  <text x="65" y="396" font-size="11" fill="#1e3a8a">• F({a}) = {a, c} (a attacks b ⇒ a defends c)</text>
  <text x="65" y="414" font-size="11" fill="#1e3a8a">• F({b}) = {b} (b defends itself against a)</text>

  <!-- Right: Semantics & Labellings Table -->
  <rect x="450" y="80" width="410" height="360" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" filter="url(#card-sh)"/>
  <text x="655" y="108" text-anchor="middle" font-size="14" font-weight="700" fill="#1e293b">Computed Extensions &amp; Legal Labellings</text>

  <!-- Semantics block -->
  <rect x="465" y="125" width="380" height="115" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="475" y="145" font-size="12" font-weight="700" fill="#0f172a">Dung Classical Semantics:</text>
  <text x="475" y="165" font-size="11.5" fill="#334155"><tspan font-weight="600">Grounded:</tspan> ∅ (Least fixed point of F)</text>
  <text x="475" y="183" font-size="11.5" fill="#334155"><tspan font-weight="600">Complete:</tspan> ∅, {b}, {a, c} (Conflict-free fixed points)</text>
  <text x="475" y="201" font-size="11.5" fill="#334155"><tspan font-weight="600">Preferred:</tspan> {b}, {a, c} (Maximal complete)</text>
  <text x="475" y="219" font-size="11.5" fill="#334155"><tspan font-weight="600">Stable &amp; Semi-Stable:</tspan> {b}, {a, c} (Range = {a, b, c})</text>

  <!-- Caminada Labelling table -->
  <rect x="465" y="255" width="380" height="170" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="475" y="275" font-size="12" font-weight="700" fill="#0f172a">Caminada 3-Valued Labellings (IN / OUT / UNDEC):</text>

  <rect x="475" y="290" width="360" height="24" fill="#f1f5f9"/>
  <text x="490" y="306" font-size="11" font-weight="700" fill="#475569">#</text>
  <text x="530" y="306" font-size="11" font-weight="700" fill="#15803d">IN (Accepted)</text>
  <text x="645" y="306" font-size="11" font-weight="700" fill="#b91c1c">OUT (Defeated)</text>
  <text x="750" y="306" font-size="11" font-weight="700" fill="#d97706">UNDEC</text>

  <line x1="475" y1="314" x2="835" y2="314" stroke="#cbd5e1"/>

  <text x="490" y="335" font-size="11" fill="#334155">1</text>
  <text x="530" y="335" font-size="11" fill="#15803d">∅</text>
  <text x="645" y="335" font-size="11" fill="#b91c1c">∅</text>
  <text x="750" y="335" font-size="11" fill="#d97706">{a, b, c}</text>

  <text x="490" y="365" font-size="11" fill="#334155">2</text>
  <text x="530" y="365" font-size="11" fill="#15803d">{b}</text>
  <text x="645" y="365" font-size="11" fill="#b91c1c">{a, c}</text>
  <text x="750" y="365" font-size="11" fill="#d97706">∅</text>

  <text x="490" y="395" font-size="11" fill="#334155">3</text>
  <text x="530" y="395" font-size="11" fill="#15803d">{a, c}</text>
  <text x="645" y="395" font-size="11" fill="#b91c1c">{b}</text>
  <text x="750" y="395" font-size="11" fill="#d97706">∅</text>

  <text x="475" y="418" font-size="10" fill="#64748b">• Argument a acceptance under preferred: Credulously accepted only</text>
</svg>"""
    write_and_verify(output_path, svg)


def generate_example_5_10_manipulation(output_path):
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 540" width="920" height="540" style="background:#ffffff; font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;">
  <defs>
    <marker id="arr-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#ef4444"/>
    </marker>
    <filter id="f-sh" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.08"/>
    </filter>
  </defs>

  <text x="460" y="30" text-anchor="middle" font-size="19" font-weight="700" fill="#0f172a">Strategic Manipulation Mechanism Design (Example 5.10 Walkthrough)</text>
  <text x="460" y="48" text-anchor="middle" font-size="12" fill="#64748b">Showing How Agent X Increases Utility from 1 to 2 by Hiding Argument α_1</text>

  <!-- PANEL 1: Truthful Disclosure -->
  <rect x="40" y="70" width="840" height="210" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" filter="url(#f-sh)"/>
  <rect x="40" y="70" width="840" height="32" rx="8" fill="#e2e8f0"/>
  <text x="55" y="92" font-size="13" font-weight="700" fill="#1e293b">SITUATION A: TRUTHFUL DISCLOSURE (All Agents Reveal Full Types)</text>
  <text x="750" y="92" font-size="12" font-weight="700" fill="#1d4ed8">GE = {α_1, α_3}</text>

  <!-- Graph nodes -->
  <!-- a1 (X) -->
  <circle cx="90" cy="160" r="26" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/>
  <text x="90" y="165" text-anchor="middle" font-size="15" font-weight="700" fill="#15803d">α_1</text>
  <text x="90" y="200" text-anchor="middle" font-size="10.5" font-weight="600" fill="#2563eb">Agent X</text>
  <text x="90" y="214" text-anchor="middle" font-size="9.5" fill="#16a34a">[IN]</text>

  <!-- a2 (Y) -->
  <circle cx="210" cy="160" r="26" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="210" y="165" text-anchor="middle" font-size="15" font-weight="700" fill="#b91c1c">α_2</text>
  <text x="210" y="200" text-anchor="middle" font-size="10.5" font-weight="600" fill="#d97706">Agent Y</text>
  <text x="210" y="214" text-anchor="middle" font-size="9.5" fill="#dc2626">[OUT]</text>

  <!-- a3 (Z) -->
  <circle cx="330" cy="160" r="26" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/>
  <text x="330" y="165" text-anchor="middle" font-size="15" font-weight="700" fill="#15803d">α_3</text>
  <text x="330" y="200" text-anchor="middle" font-size="10.5" font-weight="600" fill="#7c3aed">Agent Z</text>
  <text x="330" y="214" text-anchor="middle" font-size="9.5" fill="#16a34a">[IN]</text>

  <!-- a4 (X) -->
  <circle cx="450" cy="130" r="26" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="450" y="135" text-anchor="middle" font-size="15" font-weight="700" fill="#b91c1c">α_4</text>
  <text x="450" y="170" text-anchor="middle" font-size="10.5" font-weight="600" fill="#2563eb">Agent X</text>
  <text x="450" y="184" text-anchor="middle" font-size="9.5" fill="#dc2626">[OUT]</text>

  <!-- a5 (X) -->
  <circle cx="450" cy="210" r="26" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="450" y="215" text-anchor="middle" font-size="15" font-weight="700" fill="#b91c1c">α_5</text>
  <text x="450" y="250" text-anchor="middle" font-size="10.5" font-weight="600" fill="#2563eb">Agent X</text>
  <text x="450" y="264" text-anchor="middle" font-size="9.5" fill="#dc2626">[OUT]</text>

  <!-- Attacks -->
  <line x1="116" y1="160" x2="178" y2="160" stroke="#ef4444" stroke-width="2" marker-end="url(#arr-red)"/>
  <line x1="236" y1="160" x2="298" y2="160" stroke="#ef4444" stroke-width="2" marker-end="url(#arr-red)"/>
  <line x1="354" y1="148" x2="418" y2="135" stroke="#ef4444" stroke-width="2" marker-end="url(#arr-red)"/>
  <line x1="354" y1="172" x2="418" y2="198" stroke="#ef4444" stroke-width="2" marker-end="url(#arr-red)"/>

  <!-- Payoff Box A -->
  <rect x="520" y="115" width="340" height="145" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="535" y="138" font-size="12" font-weight="700" fill="#1e293b">Payoffs Under Truthful Reporting:</text>
  <text x="535" y="160" font-size="11.5" fill="#1e3a8a">• <tspan font-weight="600">Agent X (owns α_1, α_4, α_5):</tspan> Utility = <tspan font-weight="700" font-size="13" fill="#2563eb">1</tspan> (α_1 accepted)</text>
  <text x="535" y="180" font-size="11.5" fill="#92400e">• <tspan font-weight="600">Agent Y (owns α_2):</tspan> Utility = <tspan font-weight="700">0</tspan> (α_2 defeated by α_1)</text>
  <text x="535" y="200" font-size="11.5" fill="#5b21b6">• <tspan font-weight="600">Agent Z (owns α_3):</tspan> Utility = <tspan font-weight="700">1</tspan> (α_3 defended &amp; accepted)</text>
  <text x="535" y="224" font-size="10.5" fill="#b91c1c">[Book Erratum: Swapped Y and Z utilities in text; here fixed]</text>
  <text x="535" y="242" font-size="10" fill="#64748b">• Odd path: α_1 → α_2 → α_3 → α_4 (length 3, indirect self-defeat)</text>

  <!-- PANEL 2: Strategic Manipulation -->
  <rect x="40" y="300" width="840" height="210" rx="8" fill="#f8fafc" stroke="#ef4444" stroke-width="1.5" filter="url(#f-sh)"/>
  <rect x="40" y="300" width="840" height="32" rx="8" fill="#fee2e2"/>
  <text x="55" y="322" font-size="13" font-weight="700" fill="#b91c1c">SITUATION B: STRATEGIC MANIPULATION (Agent X Hides α_1)</text>
  <text x="740" y="322" font-size="12" font-weight="700" fill="#15803d">GE = {α_2, α_4, α_5}</text>

  <!-- Hidden a1 -->
  <circle cx="90" cy="390" r="26" fill="#f1f5f9" stroke="#94a3b8" stroke-dasharray="4 4" stroke-width="1.5"/>
  <text x="90" y="395" text-anchor="middle" font-size="14" fill="#94a3b8">α_1</text>
  <text x="90" y="430" text-anchor="middle" font-size="10" font-weight="700" fill="#ef4444">HIDDEN!</text>

  <!-- a2 (Y) -> Now unattacked! -->
  <circle cx="210" cy="390" r="26" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/>
  <text x="210" y="395" text-anchor="middle" font-size="15" font-weight="700" fill="#15803d">α_2</text>
  <text x="210" y="430" text-anchor="middle" font-size="10.5" font-weight="600" fill="#d97706">Agent Y</text>
  <text x="210" y="444" text-anchor="middle" font-size="9.5" fill="#16a34a">[IN]</text>

  <!-- a3 (Z) -> Defeated! -->
  <circle cx="330" cy="390" r="26" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="330" y="395" text-anchor="middle" font-size="15" font-weight="700" fill="#b91c1c">α_3</text>
  <text x="330" y="430" text-anchor="middle" font-size="10.5" font-weight="600" fill="#7c3aed">Agent Z</text>
  <text x="330" y="444" text-anchor="middle" font-size="9.5" fill="#dc2626">[OUT]</text>

  <!-- a4 (X) -> Accepted! -->
  <circle cx="450" cy="360" r="26" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/>
  <text x="450" y="365" text-anchor="middle" font-size="15" font-weight="700" fill="#15803d">α_4</text>
  <text x="450" y="400" text-anchor="middle" font-size="10.5" font-weight="600" fill="#2563eb">Agent X</text>
  <text x="450" y="414" text-anchor="middle" font-size="9.5" fill="#16a34a">[IN]</text>

  <!-- a5 (X) -> Accepted! -->
  <circle cx="450" cy="440" r="26" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/>
  <text x="450" y="445" text-anchor="middle" font-size="15" font-weight="700" fill="#15803d">α_5</text>
  <text x="450" y="480" text-anchor="middle" font-size="10.5" font-weight="600" fill="#2563eb">Agent X</text>
  <text x="450" y="494" text-anchor="middle" font-size="9.5" fill="#16a34a">[IN]</text>

  <!-- Attacks -->
  <line x1="236" y1="390" x2="298" y2="390" stroke="#ef4444" stroke-width="2" marker-end="url(#arr-red)"/>
  <line x1="354" y1="378" x2="418" y2="365" stroke="#94a3b8" stroke-dasharray="3 3" stroke-width="1.5"/>
  <line x1="354" y1="402" x2="418" y2="428" stroke="#94a3b8" stroke-dasharray="3 3" stroke-width="1.5"/>

  <!-- Payoff Box B -->
  <rect x="520" y="345" width="340" height="145" rx="6" fill="#ffffff" stroke="#ef4444"/>
  <text x="535" y="368" font-size="12" font-weight="700" fill="#b91c1c">Manipulated Payoffs (X Deviates):</text>
  <text x="535" y="390" font-size="11.5" fill="#1e3a8a">• <tspan font-weight="600">Agent X:</tspan> Utility = <tspan font-weight="700" font-size="14" fill="#16a34a">2</tspan> (α_4 and α_5 accepted! <tspan fill="#16a34a" font-weight="700">+1 GAIN</tspan>)</text>
  <text x="535" y="410" font-size="11.5" fill="#92400e">• <tspan font-weight="600">Agent Y:</tspan> Utility = 1 (α_2 accepted)</text>
  <text x="535" y="430" font-size="11.5" fill="#5b21b6">• <tspan font-weight="600">Agent Z:</tspan> Utility = 0 (α_3 defeated)</text>
  <text x="535" y="454" font-size="11" font-weight="700" fill="#b91c1c">⇒ THEOREM 5.3 FAILS: Grounded Mechanism is NOT Strategyproof!</text>
  <text x="535" y="472" font-size="10" fill="#64748b">• Agent X strictly benefits by withholding private argument α_1</text>
</svg>"""
    write_and_verify(output_path, svg)


def generate_example_5_11_protected_defeat(output_path):
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 480" width="920" height="480" style="background:#ffffff; font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;">
  <defs>
    <marker id="arr-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#16a34a"/>
    </marker>
    <marker id="arr-r" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#ef4444"/>
    </marker>
    <filter id="c-sh" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.08"/>
    </filter>
  </defs>

  <text x="460" y="30" text-anchor="middle" font-size="19" font-weight="700" fill="#0f172a">Protected Indirect Defeat (Discussion after Example 5.11)</text>
  <text x="460" y="48" text-anchor="middle" font-size="12" fill="#64748b">Proof That Theorem 5.4 is SUFFICIENT, But NOT NECESSARY (Protected by α_6)</text>

  <!-- Left: Graph with Protective Shield -->
  <rect x="40" y="70" width="460" height="380" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" filter="url(#c-sh)"/>
  <text x="270" y="98" text-anchor="middle" font-size="13.5" font-weight="700" fill="#1e293b">Graph Topology with Protecting Argument α_6</text>

  <!-- a1 (X) -->
  <circle cx="90" cy="190" r="24" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/>
  <text x="90" y="195" text-anchor="middle" font-size="14" font-weight="700" fill="#15803d">α_1</text>
  <text x="90" y="228" text-anchor="middle" font-size="10" font-weight="600" fill="#2563eb">Agent X</text>

  <!-- a2 (Y) -->
  <circle cx="190" cy="190" r="24" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="190" y="195" text-anchor="middle" font-size="14" font-weight="700" fill="#b91c1c">α_2</text>
  <text x="190" y="228" text-anchor="middle" font-size="10" font-weight="600" fill="#d97706">Agent Y</text>

  <!-- a3 (Z) -->
  <circle cx="290" cy="190" r="24" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="290" y="195" text-anchor="middle" font-size="14" font-weight="700" fill="#b91c1c">α_3</text>
  <text x="290" y="228" text-anchor="middle" font-size="10" font-weight="600" fill="#7c3aed">Agent Z</text>

  <!-- a4 (X) -->
  <circle cx="410" cy="150" r="24" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/>
  <text x="410" y="155" text-anchor="middle" font-size="14" font-weight="700" fill="#15803d">α_4</text>
  <text x="410" y="188" text-anchor="middle" font-size="10" font-weight="600" fill="#2563eb">Agent X</text>

  <!-- a5 (X) -->
  <circle cx="410" cy="230" r="24" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/>
  <text x="410" y="235" text-anchor="middle" font-size="14" font-weight="700" fill="#15803d">α_5</text>
  <text x="410" y="268" text-anchor="middle" font-size="10" font-weight="600" fill="#2563eb">Agent X</text>

  <!-- a6 (X) -> Protecting argument! -->
  <circle cx="290" cy="330" r="26" fill="#eff6ff" stroke="#2563eb" stroke-width="3"/>
  <text x="290" y="335" text-anchor="middle" font-size="15" font-weight="700" fill="#1e40af">α_6</text>
  <text x="290" y="372" text-anchor="middle" font-size="11" font-weight="700" fill="#2563eb">Agent X (Shield!)</text>
  <text x="290" y="388" text-anchor="middle" font-size="9.5" fill="#16a34a">[UNATTACKED]</text>

  <!-- Attacks -->
  <line x1="114" y1="190" x2="160" y2="190" stroke="#ef4444" stroke-width="2" marker-end="url(#arr-r)"/>
  <line x1="214" y1="190" x2="260" y2="190" stroke="#ef4444" stroke-width="2" marker-end="url(#arr-r)"/>
  <line x1="312" y1="180" x2="382" y2="158" stroke="#94a3b8" stroke-dasharray="3 3" stroke-width="1.5"/>
  <line x1="312" y1="200" x2="382" y2="222" stroke="#94a3b8" stroke-dasharray="3 3" stroke-width="1.5"/>

  <!-- Protective attack: a6 -> a3 (green thick arrow) -->
  <line x1="290" y1="304" x2="290" y2="222" stroke="#16a34a" stroke-width="3" marker-end="url(#arr-g)"/>
  <text x="340" y="270" text-anchor="middle" font-size="11" font-weight="700" fill="#15803d">Defeats α_3!</text>

  <rect x="55" y="405" width="430" height="32" rx="4" fill="#fef2f2" stroke="#fecaca"/>
  <text x="270" y="426" text-anchor="middle" font-size="10.5" fill="#b91c1c">Odd path α_1 → α_2 → α_3 → α_4 (len 3) still exists in the graph!</text>

  <!-- Right: Mathematical Analysis -->
  <rect x="520" y="70" width="360" height="380" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" filter="url(#c-sh)"/>
  <text x="700" y="98" text-anchor="middle" font-size="13.5" font-weight="700" fill="#1e293b">Mathematical Proof of Strategyproofness</text>

  <rect x="535" y="115" width="330" height="95" rx="6" fill="#ffffff" stroke="#ef4444"/>
  <text x="545" y="135" font-size="11.5" font-weight="700" fill="#b91c1c">1. Theorem 5.4 Check: FAILS</text>
  <text x="545" y="153" font-size="10.5" fill="#334155">• Agent X owns both α_1 and α_4</text>
  <text x="545" y="170" font-size="10.5" fill="#334155">• Directed path α_1 → α_2 → α_3 → α_4 has length 3 (odd)</text>
  <text x="545" y="188" font-size="10" font-weight="700" fill="#dc2626">⇒ Structural condition is violated</text>

  <rect x="535" y="220" width="330" height="150" rx="6" fill="#ffffff" stroke="#16a34a"/>
  <text x="545" y="240" font-size="11.5" font-weight="700" fill="#15803d">2. Theorem 5.3 Exact Check: STRATEGYPROOF!</text>
  <text x="545" y="258" font-size="10.5" fill="#334155">• α_6 has NO attackers ⇒ always accepted in GE</text>
  <text x="545" y="275" font-size="10.5" fill="#334155">• α_6 defeats α_3 ⇒ α_3 is OUT under truthfulness</text>
  <text x="545" y="292" font-size="10.5" fill="#334155">• Defeated α_3 frees α_4 and α_5 to enter GE</text>
  <text x="545" y="309" font-size="10.5" fill="#334155">• Truthful outcome: GE = {α_1, α_4, α_5, α_6}</text>
  <text x="545" y="327" font-size="11" font-weight="700" fill="#1d4ed8">• Agent X utility = 4 (Maximum possible!)</text>
  <text x="545" y="345" font-size="10" fill="#15803d">• No deviation can yield &gt; 4 ⇒ Truthfulness is dominant!</text>

  <rect x="535" y="380" width="330" height="55" rx="6" fill="#eff6ff" stroke="#bfdbfe"/>
  <text x="700" y="400" text-anchor="middle" font-size="11" font-weight="700" fill="#1e40af">CORE THEORETICAL INSIGHT:</text>
  <text x="700" y="418" text-anchor="middle" font-size="10" fill="#1e3a8a">Theorem 5.4 is SUFFICIENT, but NOT NECESSARY.</text>
  <text x="700" y="430" text-anchor="middle" font-size="9" fill="#64748b">Verified on 898 empirical instances in Part 3!</text>
</svg>"""
    write_and_verify(output_path, svg)


def generate_parity_bfs_state_graph(output_path):
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 480" width="920" height="480" style="background:#ffffff; font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;">
  <defs>
    <marker id="arr-b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb"/>
    </marker>
    <marker id="arr-m" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#7c3aed"/>
    </marker>
    <filter id="p-sh" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.08"/>
    </filter>
  </defs>

  <text x="460" y="30" text-anchor="middle" font-size="19" font-weight="700" fill="#0f172a">2-State Parity BFS Traversal on G × Z_2 (Theorem 5.4 Odd-Path Verification)</text>
  <text x="460" y="48" text-anchor="middle" font-size="12" fill="#64748b">Handling Graph Cycles, Self-Attacks, and Arbitrary Directed Walk Parities</text>

  <!-- Left: State space illustration -->
  <rect x="40" y="70" width="480" height="380" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" filter="url(#p-sh)"/>
  <text x="280" y="98" text-anchor="middle" font-size="13.5" font-weight="700" fill="#1e293b">2-State Parity Graph Construction: (node, parity)</text>

  <!-- Parity 0 Layer (Even) -->
  <rect x="60" y="120" width="440" height="100" rx="6" fill="#f0fdf4" stroke="#86efac"/>
  <text x="75" y="142" font-size="12" font-weight="700" fill="#166534">PARITY 0 LAYER (Even-length walks from start):</text>

  <circle cx="120" cy="180" r="22" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
  <text x="120" y="185" text-anchor="middle" font-size="11.5" font-weight="700" fill="#15803d">(a, 0)</text>

  <circle cx="250" cy="180" r="22" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
  <text x="250" y="185" text-anchor="middle" font-size="11.5" font-weight="700" fill="#15803d">(c, 0)</text>

  <circle cx="380" cy="180" r="22" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
  <text x="380" y="185" text-anchor="middle" font-size="11.5" font-weight="700" fill="#15803d">(b, 0)</text>

  <!-- Parity 1 Layer (Odd) -->
  <rect x="60" y="270" width="440" height="100" rx="6" fill="#fef2f2" stroke="#fecaca"/>
  <text x="75" y="292" font-size="12" font-weight="700" fill="#991b1b">PARITY 1 LAYER (Odd-length walks ⇒ Target of Thm 5.4 check):</text>

  <circle cx="185" cy="330" r="22" fill="#ffffff" stroke="#dc2626" stroke-width="2"/>
  <text x="185" y="335" text-anchor="middle" font-size="11.5" font-weight="700" fill="#b91c1c">(b, 1)</text>

  <circle cx="315" cy="330" r="22" fill="#ffffff" stroke="#dc2626" stroke-width="2"/>
  <text x="315" y="335" text-anchor="middle" font-size="11.5" font-weight="700" fill="#b91c1c">(a, 1)</text>

  <circle cx="445" cy="330" r="22" fill="#ffffff" stroke="#dc2626" stroke-width="2"/>
  <text x="445" y="335" text-anchor="middle" font-size="11.5" font-weight="700" fill="#b91c1c">(c, 1)</text>

  <!-- Cross-layer edges: Every edge in AF flips parity (0 -> 1 -> 0 -> 1) -->
  <line x1="135" y1="195" x2="170" y2="310" stroke="#2563eb" stroke-width="2" marker-end="url(#arr-b)"/>
  <line x1="200" y1="315" x2="235" y2="200" stroke="#2563eb" stroke-width="2" marker-end="url(#arr-b)"/>
  <line x1="265" y1="195" x2="300" y2="310" stroke="#2563eb" stroke-width="2" marker-end="url(#arr-b)"/>

  <!-- Self-attack illustration -->
  <rect x="60" y="385" width="440" height="50" rx="6" fill="#ffffff" stroke="#94a3b8"/>
  <text x="75" y="405" font-size="11" font-weight="700" fill="#1e293b">Self-Attack Handling (α → α):</text>
  <text x="75" y="422" font-size="10" fill="#64748b">Transitions from (α, 0) directly to (α, 1) ⇒ Length 1 (Odd self-defeat!)</text>

  <!-- Right: Why Standard BFS Fails & Properties -->
  <rect x="540" y="70" width="340" height="380" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" filter="url(#p-sh)"/>
  <text x="710" y="98" text-anchor="middle" font-size="13.5" font-weight="700" fill="#1e293b">Algorithmic Advantages</text>

  <rect x="555" y="120" width="310" height="95" rx="6" fill="#ffffff" stroke="#ef4444"/>
  <text x="565" y="140" font-size="11.5" font-weight="700" fill="#b91c1c">Why Naive BFS with visited[u] Fails:</text>
  <text x="565" y="158" font-size="10.5" fill="#334155">• A vertex can be reached first via an EVEN path</text>
  <text x="565" y="175" font-size="10.5" fill="#334155">• Standard BFS marks it visited and skips it</text>
  <text x="565" y="193" font-size="10" font-weight="700" fill="#dc2626">⇒ Completely misses subsequent ODD paths!</text>

  <rect x="555" y="225" width="310" height="110" rx="6" fill="#ffffff" stroke="#16a34a"/>
  <text x="565" y="245" font-size="11.5" font-weight="700" fill="#15803d">2-State BFS Solves Cycles in O(|A|+|R|):</text>
  <text x="565" y="265" font-size="10.5" fill="#334155">• Tracks state: <tspan font-weight="700">(node, parity)</tspan></text>
  <text x="565" y="283" font-size="10.5" fill="#334155">• Each node can be visited at most TWICE (0 and 1)</text>
  <text x="565" y="301" font-size="10.5" fill="#334155">• Guaranteed termination on arbitrary cyclic graphs</text>
  <text x="565" y="319" font-size="10" fill="#047857">• Catches odd walks and self-attacks effortlessly</text>

  <rect x="555" y="345" width="310" height="90" rx="6" fill="#eff6ff" stroke="#bfdbfe"/>
  <text x="565" y="365" font-size="11" font-weight="700" fill="#1e40af">Condition Verification Rule:</text>
  <text x="565" y="385" font-size="10.5" fill="#1e3a8a">∀ agent i, ∀ α, β ∈ A_i:</text>
  <text x="565" y="403" font-size="10.5" font-weight="700" fill="#b91c1c">(α, 0) reaches (β, 1) ⇒ Condition FAILS!</text>
  <text x="565" y="421" font-size="10" fill="#64748b">(Includes α = β for self-attacks and odd cycles)</text>
</svg>"""
    write_and_verify(output_path, svg)


def main():
    dirs = [
        "C:/Users/ASUS/Downloads/prog/Argumentation/diagrams",
        "C:/Users/ASUS/.gemini/antigravity/scratch/argumentation_engine/diagrams",
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        generate_system_architecture(os.path.join(d, "system_architecture.svg"))
        generate_semantics_labelling(os.path.join(d, "semantics_labelling_example.svg"))
        generate_example_5_10_manipulation(os.path.join(d, "example_5_10_manipulation.svg"))
        generate_example_5_11_protected_defeat(os.path.join(d, "example_5_11_protected_defeat.svg"))
        generate_parity_bfs_state_graph(os.path.join(d, "parity_bfs_state_graph.svg"))

if __name__ == "__main__":
    main()
