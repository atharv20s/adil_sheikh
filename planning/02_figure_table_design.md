# Figure & Table Design Book
## IDS → BFT Blockchain Comparative Paper

> Every figure and table is designed before a single line of the paper is written.
> All cells are left blank until experiments are complete.

---

## FIGURES

---

### Figure 1: AMI System Architecture

| Field | Specification |
|-------|---------------|
| **Purpose** | Show the IEEE 33-bus AMI architecture with smart meters, data concentrators, MDMS, and communication channels. Establish the physical system under study. |
| **Type** | System diagram |
| **Variables** | None (static architecture) |
| **Software** | draw.io or TikZ |
| **Caption** | "IEEE 33-bus distribution system with 50 EVs, 3854 sensors, and 51 validator nodes. Smart meters communicate via IEEE 802.15.4 to data concentrators, which relay data to the centralized MDMS (IDS) or distributed validator network (BFT)." |
| **Referenced Section** | Section III (System Architecture) |
| **Experiment** | None (context diagram) |
| **Estimated Size** | Full column width |
| **Status** | Existing: `fig_comparative_workflow.png` can be adapted |

---

### Figure 2: Architectural Comparison — IDS vs. BFT Blockchain

| Field | Specification |
|-------|---------------|
| **Purpose** | Side-by-side comparison showing data flow in centralized IDS (SM → SVM → TFPG → MDMS → Response) vs. distributed BFT (SM → Hash → P2P → Consensus → Append). Highlight the SPOF in IDS. |
| **Type** | Dual-panel flow diagram |
| **Variables** | None (architecture comparison) |
| **Software** | draw.io |
| **Caption** | "Architectural comparison: (a) Centralized two-stage IDS with MDMS single point of failure, (b) Distributed BFT blockchain consensus with no SPOF. Red node indicates the centralized coordinator vulnerability." |
| **Referenced Section** | Section III-B |
| **Experiment** | None (design diagram) |
| **Estimated Size** | Full page width (two-column span) |
| **Status** | **NEW** — must be created |

---

### Figure 3: Attack Probability vs. Sensor Security ($x$) — Sheikh Model

| Field | Specification |
|-------|---------------|
| **Purpose** | Show $P_{TA}$ (without blockchain) and $P_{TAb}$ (with blockchain) as functions of $x \in [0.90, 0.999]$ to visualize the 170 OoM gap. |
| **Type** | Dual-axis line plot (log scale for $P_{TAb}$) |
| **X-axis** | $x$ (sensor security parameter), range $[0.90, 0.999]$ |
| **Y-axis (left)** | $P_{TA}$ (linear scale) |
| **Y-axis (right)** | $\log_{10}(P_{TAb})$ (log scale) |
| **Lines** | $P_{TA}$ (red, dashed), $P_{TAb}$ (blue, solid) |
| **Caption** | "Attack probability as a function of sensor security parameter $x$. Without blockchain (red): $P_{TA} \approx 0.005$ at $x = 0.95$. With blockchain (blue): $P_{TAb} \approx 10^{-173}$, demonstrating a static security gain of ~170 orders of magnitude." |
| **Referenced Section** | Section VI-A (Sheikh benchmark) |
| **Experiment** | E1 |
| **Estimated Size** | Single column |
| **Status** | Existing: `fig_w2_pta_no_blockchain.png`, `fig_w2_ptab_with_blockchain.png` — adapt for combined plot |

---

### Figure 4: SPOF Risk — $P_{Byz}$ vs. Validator Compromise Probability

| Field | Specification |
|-------|---------------|
| **Purpose** | Show how $P_{Byz}^{BFT}$ (binomial tail) varies with $p_c$ and compare to $P_{Byz}^{IDS} = 1.0$ (horizontal line). |
| **Type** | Semi-log line plot |
| **X-axis** | $p_c$ (per-validator compromise probability), range $[0.01, 0.20]$ |
| **Y-axis** | $P_{Byz}$ (log scale) |
| **Lines** | IDS baseline: $P_{Byz} = 1.0$ (red, horizontal). BFT: binomial tail curve (blue). |
| **Annotations** | Shaded region below $10^{-5}$ threshold. Arrow indicating "BFT operating region." |
| **Caption** | "Byzantine failure probability: centralized IDS coordinator ($P_{Byz} = 1.0$, red) vs. distributed BFT network ($n = 51$, $f = 16$, blue). BFT maintains $P_{Byz} < 10^{-5}$ for $p_c < 0.15$." |
| **Referenced Section** | Section VII-B |
| **Experiment** | E3 |
| **Estimated Size** | Single column |
| **Status** | **NEW** — must be created |

---

### Figure 5: Per-Attack Comparison Bar Chart (IDS vs. BFT)

| Field | Specification |
|-------|---------------|
| **Purpose** | Grouped bar chart showing $P_{atk}^{IDS}$ vs. $P_{atk}^{BFT}$ for all 12 attack vectors side by side. |
| **Type** | Grouped horizontal bar chart (log scale) |
| **X-axis** | $P_{atk}$ (log scale) |
| **Y-axis** | Attack type (12 categories) |
| **Bars** | Red (IDS), Blue (BFT) per attack |
| **Annotations** | "Eliminated" label for Replay ($P = 0$). "SPOF" label for Sybil/Byz IDS bars. |
| **Caption** | "Per-attack probability comparison: centralized IDS (red) vs. BFT blockchain (blue). Blockchain eliminates replay attacks, reduces Sybil/Byzantine from 1.0 to $\sim 10^{-10}$, and reduces all other vectors." |
| **Referenced Section** | Section VII-A |
| **Experiment** | E2 |
| **Estimated Size** | Full page width |
| **Status** | Existing: `fig18_without_vs_with_blockchain.png` — adapt with IDS framing |

---

### Figure 6: Consensus-Dependent Security Heatmap

| Field | Specification |
|-------|---------------|
| **Purpose** | $9 \times 12$ heatmap showing per-protocol, per-attack probabilities with color scale. |
| **Type** | Heatmap (log-scale color mapping) |
| **X-axis** | Attack vector (12 columns) |
| **Y-axis** | Protocol (9 rows + "Without BC" row) |
| **Color scale** | Green (low probability) → Red (high probability), log scale |
| **Caption** | "Consensus-dependent joint security heatmap. Each cell shows $\log_{10}(P_j^{Algo})$. Darker green indicates stronger defense. The 'Without BC' row shows the centralized IDS baseline." |
| **Referenced Section** | Section VIII |
| **Experiment** | E7 |
| **Estimated Size** | Full page width |
| **Status** | Existing: `comparison_heatmap.png` — add IDS baseline row |

---

### Figure 7: Latency vs. $P_{secure}$ Scatter Plot

| Field | Specification |
|-------|---------------|
| **Purpose** | Show the exponential decay of system security with consensus latency. Identify the high-security/low-latency region for AMI. |
| **Type** | Scatter plot with exponential fit curve |
| **X-axis** | Consensus latency $L$ (ms), log scale |
| **Y-axis** | $P_{secure}$ |
| **Points** | 9 protocols, color-coded by group (G1–G4) |
| **Annotations** | Shaded "AMI Operating Region" box ($L < 1000$ ms, $P_{secure} > 0.85$) |
| **Caption** | "Latency vs. overall security for 9 BFT consensus protocols under Poisson temporal attack model ($\lambda = 20$). Sub-second protocols (Tower BFT, RVR) cluster in the high-security region." |
| **Referenced Section** | Section VIII-A |
| **Experiment** | E4 |
| **Estimated Size** | Single column |
| **Status** | Existing: `fig_latency_vs_psecure.png` |

---

### Figure 8: Temporal Vulnerability Curve

| Field | Specification |
|-------|---------------|
| **Purpose** | Show $P_{temporal}$ as a continuous function of latency, with protocol points annotated. |
| **Type** | Line plot with annotated points |
| **X-axis** | Consensus latency $L$ (ms) |
| **Y-axis** | $P_{temporal}$ |
| **Line** | $P_{temporal} = 1 - e^{-\lambda L P_{TA}}$ curve |
| **Points** | 9 protocols marked on curve |
| **Caption** | "Temporal vulnerability exposure under Poisson attack arrival ($\lambda = 20$, $P_{TA} = 0.005$). Protocols exceeding 2000 ms lose >20% of static security." |
| **Referenced Section** | Section VIII-A |
| **Experiment** | E4 |
| **Estimated Size** | Single column |
| **Status** | Existing: `fig_ptemporal_vs_latency.png` |

---

### Figure 9: Sensitivity Tornado Diagram

| Field | Specification |
|-------|---------------|
| **Purpose** | Show relative contribution of each parameter to $P_{secure}$ variation. |
| **Type** | Tornado / horizontal bar chart |
| **X-axis** | $\Delta P_{secure}$ (absolute change) |
| **Y-axis** | Parameter name |
| **Bars** | One per parameter, sorted by magnitude |
| **Caption** | "Parameter sensitivity ranking. Latency and attack rate dominate system security variation (~98%), confirming that temporal factors are decisive." |
| **Referenced Section** | Section IX-B |
| **Experiment** | E5 |
| **Estimated Size** | Single column |
| **Status** | Existing: `fig_sensitivity_ranking.png` |

---

### Figure 10: $\eta$ Sensitivity Table-Plot

| Field | Specification |
|-------|---------------|
| **Purpose** | Show $P_{secure}$ for 3 representative protocols across $\eta \in [0.05, 0.25]$. |
| **Type** | Multi-line plot |
| **X-axis** | $\eta$ (spatial validation factor) |
| **Y-axis** | $P_{secure}$ |
| **Lines** | Classic PBFT, Tower BFT, RVR |
| **Caption** | "Sensitivity of $P_{secure}$ to spatial validation factor $\eta$. Rankings remain stable across the full range." |
| **Referenced Section** | Section IX-B |
| **Experiment** | E5 |
| **Estimated Size** | Single column |
| **Status** | **NEW** — create from existing table data |

---

### Figure 11: $\beta$ Sensitivity Table-Plot

| Field | Specification |
|-------|---------------|
| **Purpose** | Show $P_{secure}$ for 3 representative protocols across $\beta \in [0.05, 0.25]$. |
| **Type** | Multi-line plot |
| **X-axis** | $\beta$ (voting phase factor) |
| **Y-axis** | $P_{secure}$ |
| **Lines** | Classic PBFT, Tower BFT, RVR |
| **Caption** | "Sensitivity of $P_{secure}$ to voting phase factor $\beta$. Protocol rankings are preserved." |
| **Referenced Section** | Section IX-B |
| **Experiment** | E5 |
| **Estimated Size** | Single column |
| **Status** | **NEW** — create from existing table data |

---

### Figure 12: Monte Carlo Convergence

| Field | Specification |
|-------|---------------|
| **Purpose** | Show MC estimates converging to analytical values as trial count increases. |
| **Type** | Multi-line convergence plot |
| **X-axis** | Number of trials (log scale, $10^1$ to $10^6$) |
| **Y-axis** | Estimated probability |
| **Lines** | One per key metric (sensor, comm, compromise), with analytical horizontal reference lines |
| **Caption** | "Monte Carlo convergence: estimated probabilities converge to analytical predictions within 0.5% at $10^6$ trials." |
| **Referenced Section** | Section IX-C |
| **Experiment** | E6 |
| **Estimated Size** | Single column |
| **Status** | Existing: `fig_monte_carlo_validation.png` |

---

### Figure 13: Message Complexity Comparison

| Field | Specification |
|-------|---------------|
| **Purpose** | Compare message counts across protocols, highlighting OM(m)'s exponential growth. |
| **Type** | Bar chart (log scale) |
| **X-axis** | Protocol |
| **Y-axis** | Message count (log scale) |
| **Caption** | "Message complexity comparison ($n = 51$). OM(m) requires $\sim 10^{27}$ messages, making real-time AMI deployment infeasible. Sub-second protocols achieve $\mathcal{O}(n)$." |
| **Referenced Section** | Section VIII-C |
| **Experiment** | E9 |
| **Estimated Size** | Single column |
| **Status** | Existing: `fig_message_complexity.png` |

---

### Figure 14: Static Security Gain Visualization

| Field | Specification |
|-------|---------------|
| **Purpose** | Dramatic visualization of the 170 OoM security improvement. |
| **Type** | Annotated comparison (log-scale bar or magnitude diagram) |
| **Caption** | "Static security gain: blockchain reduces attack probability from $P_{TA} \approx 0.005$ to $P_{TAb} \approx 10^{-173}$, an improvement of ~170 orders of magnitude." |
| **Referenced Section** | Section VI-A |
| **Experiment** | E1 |
| **Estimated Size** | Single column |
| **Status** | Existing: `fig_security_gain.png` |

---

## Figure Count Summary

| Status | Count |
|--------|-------|
| Existing (reuse directly) | 8 |
| Existing (adapt/relabel) | 3 |
| New (must create) | 3 |
| **Total** | **14** |

---

## TABLES

---

### Table I: Baseline Probability Parameters

| Column | Description | Units |
|--------|-------------|-------|
| Parameter | Symbol ($x$, $y$, $z$, etc.) | — |
| Physical Meaning | What it represents | — |
| Baseline Value | Numerical value | — |
| Range (Sensitivity) | Sweep range for E5 | — |
| Source/Citation | Literature reference | — |

**Rows:** $x$, $m$, $y$, $z$, $p_{dos}$, $p_{ddos}$, $p_{key}$, $P_{SCADA}$, $P_R$, $p_c$, $n$, $f$, $n_{sen}$

**Purpose:** Single reference table for all parameters. Appears early in paper.

**Referenced Section:** Section III-D

**Experiment:** All

---

### Table II: Consensus Calibration Parameters

| Column | Description | Units |
|--------|-------------|-------|
| Parameter | Symbol ($\eta$, $\beta$, $\omega_{credit}$, $\tau_{dos}$, $\tau_{recv}$, $\tau_{scada}$) | — |
| Value | Baseline value | — |
| Physical Rationale | Engineering justification | — |

**Rows:** $\eta$, $\beta$, $\omega_{credit}$, $\tau_{dos}$, $\tau_{recv}$, $\tau_{scada}$

**Purpose:** Justify calibration constants.

**Referenced Section:** Section VI-B

**Experiment:** E7, E8

---

### Table III: Sheikh 4-Component Model Reproduction

| Column | Units |
|--------|-------|
| Configuration (Without BC / With BC) | — |
| $P_{SA}$ | probability |
| $P_{CA}$ | probability |
| $P_{SCADA}$ | probability |
| $P_R$ | probability |
| $P_{TA}$ / $P_{TAb}$ | probability |
| Static Gain | OoM |

**Rows:** Without Blockchain, With Blockchain

**Purpose:** Reproduce Sheikh's baseline exactly.

**Referenced Section:** Section VI-A

**Experiment:** E1

**Cell values:** _BLANK — fill after E1_

---

### Table IV: Attack Coverage Matrix

| Column | Description |
|--------|-------------|
| Attack Type | 12 attack names |
| IDS Coverage | ✓ or ✗ |
| BFT Coverage | ✓ or ✗ |
| IDS Defense Mechanism | Text description (or "None") |
| BFT Defense Mechanism | Text description |

**Rows:** 12 attacks

**Purpose:** Qualitative coverage comparison.

**Referenced Section:** Section VII-C

**Experiment:** E2

**Cell values:** _BLANK — fill after E2_

---

### Table V: Attack-by-Attack Quantitative Comparison

| Column | Units |
|--------|-------|
| Attack Vector | — |
| $P_{atk}^{IDS}$ (Without Blockchain) | probability |
| $P_{atk}^{BFT}$ (With Blockchain) | probability |
| Reduction Factor | ratio |
| Blockchain Defense Mechanism | text |

**Rows:** 12 attacks + System Compromise total

**Purpose:** Central quantitative comparison table.

**Referenced Section:** Section VI-A

**Experiment:** E2

**Cell values:** _BLANK — fill after E2_

---

### Table VI: SPOF Risk Comparison

| Column | Units |
|--------|-------|
| Architecture | IDS / BFT |
| $P_{Byz}$ | probability |
| Coordinator Model | centralized / distributed |
| Reduction Factor | ratio |

**Rows:** IDS, BFT

**Purpose:** Quantify SPOF elimination.

**Referenced Section:** Section VII-B

**Experiment:** E3

**Cell values:** _BLANK — fill after E3_

---

### Table VII: Consensus-Dependent Joint Security ($9 \times 14$ Matrix)

| Columns | Units |
|---------|-------|
| Protocol | — |
| $P_{Sensor}$ through $P_{Receiver}$ (12 attacks) | probability |
| $P_{Compromise}$ | probability |
| $P_{secure}$ | probability |

**Rows:** 9 protocols + "Without BC" baseline

**Purpose:** The master protocol comparison table.

**Referenced Section:** Section VIII

**Experiment:** E7

**Cell values:** _BLANK — fill after E7_

---

### Table VIII: Protocol Security Ranking

| Column | Units |
|--------|-------|
| Rank | integer |
| Protocol | — |
| $P_{secure}$ | probability |
| $P_{temporal}$ | probability |
| Latency $L$ | ms |
| TPS | transactions/s |
| Message Complexity | Big-O notation |

**Rows:** 9 protocols ranked by $P_{secure}$

**Purpose:** Summary ranking table.

**Referenced Section:** Section VIII-A

**Experiment:** E4

**Cell values:** _BLANK — fill after E4_

---

### Table IX: $\eta$ Sensitivity

| Columns | $\eta = 0.05$ | $\eta = 0.10$ | $\eta = 0.15$ | $\eta = 0.20$ | $\eta = 0.25$ |
|---------|:---:|:---:|:---:|:---:|:---:|
| Classic PBFT | | | | | |
| Tower BFT | | | | | |
| RVR | | | | | |

**Purpose:** Demonstrate ranking stability.

**Referenced Section:** Section IX-B

**Experiment:** E5

---

### Table X: $\beta$ Sensitivity

| Columns | $\beta = 0.05$ | $\beta = 0.10$ | $\beta = 0.15$ | $\beta = 0.20$ | $\beta = 0.25$ |
|---------|:---:|:---:|:---:|:---:|:---:|
| Classic PBFT | | | | | |
| Tower BFT | | | | | |
| RVR | | | | | |

**Purpose:** Demonstrate ranking stability.

**Referenced Section:** Section IX-B

**Experiment:** E5

---

### Table XI: Monte Carlo Validation

| Column | Units |
|--------|-------|
| Metric | — |
| Analytical Value | probability |
| Monte Carlo Mean | probability |
| MC Std Dev | probability |
| Relative Error | % |

**Rows:** 6 key metrics

**Purpose:** Validate analytical framework.

**Referenced Section:** Section IX-C

**Experiment:** E6

**Cell values:** _BLANK — fill after E6_

---

### Table XII: Ablation Study

| Columns | Normal | No Credit | No VRF | No Latency |
|---------|:---:|:---:|:---:|:---:|
| Classic PBFT | | | | |
| Tower BFT | | | | |
| RVR | | | | |

**Purpose:** Isolate feature contributions.

**Referenced Section:** Section IX-D

**Experiment:** E8

---

### Table XIII: Computational Overhead Comparison

| Column | IDS | BFT Blockchain |
|--------|-----|----------------|
| Training | | |
| Runtime Operations | | |
| Message Complexity | | |
| Latency Type | | |
| Scalability | | |
| Adaptability | | |

**Purpose:** Side-by-side computational feasibility.

**Referenced Section:** Section VII-E

**Experiment:** E9

---

### Table XIV: Message Complexity Formulations

| Column | Units |
|--------|-------|
| Protocol | — |
| Complexity Formula | Big-O |
| Message Count ($n = 51$) | integer |

**Rows:** 9 protocols

**Purpose:** Quantitative message overhead.

**Referenced Section:** Section VIII-C

**Experiment:** E9

---

## Table Count Summary

| Status | Count |
|--------|-------|
| Inherited (data exists, relabel) | 8 |
| New (must compute) | 6 |
| **Total** | **14** |
