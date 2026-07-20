# Experimental Specification Document (ESD)
## IDS → BFT Blockchain Comparative Paper

> Every experiment is fully defined before implementation.
> No numerical results are assumed. All outputs are placeholders until experiments run.

---

## Research Questions

| ID | Research Question |
|----|-------------------|
| RQ1 | Does BFT blockchain consensus provide structurally superior static security compared to a two-stage IDS (SVM+TFPG) for AMI, measured across 12 parallel cyber-physical attack vectors? |
| RQ2 | How does the choice of BFT consensus protocol affect the realized temporal security gains, and which protocols meet AMI latency constraints? |
| RQ3 | Is the comparative advantage of BFT over IDS robust across parameter variations in sensor security, attack rates, and consensus calibration? |
| RQ4 | What is the quantitative SPOF risk reduction when replacing a centralized MDMS coordinator with distributed BFT validators? |

## Hypotheses

| ID | Hypothesis | Null Hypothesis | Test |
|----|-----------|-----------------|------|
| H1 | BFT blockchain reduces the static attack probability by ≥100 OoM compared to centralized IDS under Sheikh's 4-component model. | The reduction is <100 OoM. | E1 (analytical), E6 (Monte Carlo) |
| H2 | Sub-second BFT protocols (Tower BFT, RVR) preserve ≥90% of the static security gain under Poisson temporal attack model. | Preservation is <90%. | E4 (analytical) |
| H3 | The comparative security advantage of BFT over IDS is robust (relative ranking unchanged) across $x \in [0.90, 0.999]$, $y \in [0.01, 0.20]$, $z \in [0.05, 0.45]$. | At least one parameter sweep reverses the advantage. | E5 (sensitivity sweep) |
| H4 | Distributed BFT reduces SPOF probability from $P_{Byz} = 1.0$ (centralized) to $P_{Byz} < 10^{-5}$ (distributed). | $P_{Byz} \geq 10^{-5}$ under BFT. | E3 (analytical) |
| H5 | BFT blockchain addresses ≥10 of the 12 identified attack vectors structurally, vs. ≤4 for the two-stage IDS. | BFT addresses <10, or IDS addresses >4. | E2 (qualitative + quantitative) |

---

## Experiment E1: Sheikh 4-Component Quantitative Benchmark

| Field | Specification |
|-------|---------------|
| **Research Question** | RQ1 |
| **Hypothesis** | H1 |
| **Objective** | Reproduce Sheikh et al.'s 4-component model (Eq. 14–21) under both centralized (IDS) and blockchain configurations to establish the primary quantitative security benchmark. |
| **What exactly are we measuring?** | $P_{TA}$ (without blockchain) and $P_{TAb}$ (with blockchain) at $x = 0.95$, $n_{sen} = 3854$. Static security gain = $P_{TA} / P_{TAb}$. |
| **Inputs** | $x = 0.95$, $n_{sen} = 3854$, $P_{SCADA} = 0.01$, $P_R = 0.01$, weights = $(0.25, 0.25, 0.25, 0.25)$ |
| **Outputs** | $P_{TA}$, $P_{TAb}$, $\log_{10}(P_{TAb})$, Static Security Gain (OoM) |
| **Independent variables** | $x$ (swept in E5 for sensitivity) |
| **Dependent variables** | $P_{TA}$, $P_{TAb}$, gain magnitude |
| **Controlled variables** | $n_{sen} = 3854$, $P_{SCADA} = 0.01$, $P_R = 0.01$, weights fixed at $(0.25, 0.25, 0.25, 0.25)$ |
| **Statistical tests** | Analytical closed-form computation. Monte Carlo validation in E6. |
| **Existing code** | `probabilistic_model.py`: `p_ta_no_blockchain()`, `p_tab_blockchain()`, `log10_p_tab_blockchain()` |
| **Figures** | Figure 3 (Attack probability vs. $x$ sweep) |
| **Tables** | Table III (Sheikh model reproduction) |
| **Inherited / Adapted / New** | **Inherited** from Sheikh et al. 2020 (Eq. 14–21). Reproduced without modification. |
| **Expected interpretation** | Placeholder. Value of $P_{TA}$ and $P_{TAb}$ to be reported after computation. The gain direction (improvement) is hypothesized but magnitude is not assumed. |

---

## Experiment E2: 12-Attack Coverage Comparison (IDS vs. BFT)

| Field | Specification |
|-------|---------------|
| **Research Question** | RQ1, RQ4 |
| **Hypothesis** | H5 |
| **Objective** | Map each of the 12 cyber-physical attack vectors to the defense mechanism available under (a) centralized IDS and (b) BFT blockchain, and compute per-attack probability reductions. |
| **What exactly are we measuring?** | For each of 12 attack vectors: baseline probability (IDS/centralized), blockchain-mitigated probability, percentage reduction, and whether the defense is structural or detection-based. |
| **Inputs** | $x = 0.95$, $m = 10$, $y = 0.05$, $z = 0.15$, $p_{dos} = 0.20$, $p_{ddos} = 0.35$, $p_{key} = 0.01$, $P_{SCADA} = 0.01$, $P_R = 0.01$, $p_c = 0.05$, $n = 51$, $f = 16$ |
| **Outputs** | 12-row comparison table: $P_{atk}^{IDS}$, $P_{atk}^{BFT}$, reduction factor, defense type (structural/detection/none) |
| **Independent variables** | Attack type (categorical, 12 levels) |
| **Dependent variables** | $P_{atk}^{IDS}$, $P_{atk}^{BFT}$, reduction ratio |
| **Controlled variables** | All baseline parameters fixed per Table I |
| **Statistical tests** | Analytical computation. No stochastic test needed (deterministic formulas). |
| **Existing code** | `probabilistic_model.py`: `p_compromise_no_bc_12attack()`, `p_compromise_bc_12attack()` |
| **Figures** | Figure 5 (Comparative bar chart: IDS vs BFT per-attack) |
| **Tables** | Table V (Attack-by-Attack Comparison), Table IV (Attack Coverage Matrix) |
| **Inherited / Adapted / New** | **Adapted**: The 12 attack formulations are from our prior work (BFT comparison paper). **New**: The IDS column and coverage matrix are new to this paper. |
| **Expected interpretation** | Placeholder. The number of attacks structurally addressed by each paradigm to be reported after analysis. |

---

## Experiment E3: SPOF Vulnerability Analysis

| Field | Specification |
|-------|---------------|
| **Research Question** | RQ4 |
| **Hypothesis** | H4 |
| **Objective** | Quantify the Single Point of Failure risk under centralized IDS ($P_{Byz}^{IDS}$) vs. distributed BFT ($P_{Byz}^{BFT}$) using binomial tail probability. |
| **What exactly are we measuring?** | $P_{Byz}^{IDS} = 1.0$ (by definition: centralized coordinator). $P_{Byz}^{BFT} = \sum_{i=f+1}^{n} \binom{n}{i} p_c^i (1-p_c)^{n-i}$. Reduction factor. |
| **Inputs** | $n = 51$, $f = 16$, $p_c = 0.05$ (baseline), $p_c$ swept $[0.01, 0.20]$ |
| **Outputs** | $P_{Byz}^{BFT}$ at baseline, $P_{Byz}^{BFT}$ across $p_c$ sweep, reduction factor |
| **Independent variables** | $p_c$ (per-validator compromise probability) |
| **Dependent variables** | $P_{Byz}^{BFT}$ |
| **Controlled variables** | $n = 51$, $f = 16$ |
| **Statistical tests** | Analytical binomial tail. Exact computation (no approximation). |
| **Existing code** | `probabilistic_model.py`: Binomial tail in `p_compromise_bc_12attack()` (Sybil/Byz calculation) |
| **Figures** | Figure 4 ($P_{Byz}$ vs. $p_c$ sweep) |
| **Tables** | Table VI (SPOF Risk Comparison) |
| **Inherited / Adapted / New** | **Inherited**: Binomial tail from Castro & Liskov 1999. **Adapted**: Application to AMI SPOF comparison is new. |
| **Expected interpretation** | Placeholder. |

---

## Experiment E4: Temporal Vulnerability Window (9 Protocols)

| Field | Specification |
|-------|---------------|
| **Research Question** | RQ2 |
| **Hypothesis** | H2 |
| **Objective** | Evaluate how consensus latency affects the realized security gain for each of 9 BFT protocols under Poisson temporal attack model. |
| **What exactly are we measuring?** | $P_{temporal}(\lambda, L)$ and $P_{secure}$ for each protocol at $\lambda = 20$ attacks/s. |
| **Inputs** | Protocol latencies from `protocols.json` (9 protocols). $\lambda = 20$, $P_{TA} = 0.005$, $P_{TAb} \approx 10^{-173}$, $P_{other} = 0.05$, $\rho = 0.3$. |
| **Outputs** | Per-protocol: $P_{temporal}$, $P_{secure}$, security preservation ratio ($P_{secure} / P_{secure,max}$) |
| **Independent variables** | Protocol (categorical, 9 levels), $L$ (latency in ms) |
| **Dependent variables** | $P_{temporal}$, $P_{secure}$ |
| **Controlled variables** | $\lambda = 20$, $x = 0.95$, $n_{sen} = 3854$, $P_{other} = 0.05$ |
| **Statistical tests** | Analytical Poisson model. No stochastic sampling. |
| **Existing code** | `probabilistic_model.py`: `p_temporal_poisson()`, `p_secure()`. `protocols.json` for latency values. |
| **Figures** | Figure 7 (Latency vs. $P_{secure}$ scatter), Figure 8 ($P_{temporal}$ vs. latency curve) |
| **Tables** | Table VIII (Protocol Security Ranking) |
| **Inherited / Adapted / New** | **Inherited**: STSF temporal model from prior BFT comparison work. **Adapted**: Recontextualized as AMI-specific evaluation. |
| **Expected interpretation** | Placeholder. The percentage of static security preserved by sub-second protocols to be reported. |

---

## Experiment E5: Sensitivity Analysis

| Field | Specification |
|-------|---------------|
| **Research Question** | RQ3 |
| **Hypothesis** | H3 |
| **Objective** | Verify that the comparative advantage of BFT over IDS is robust across parameter variations. |
| **What exactly are we measuring?** | (a) Static parameters: $P_{Compromise}^{IDS}$ and $P_{Compromise}^{BFT}$ as $x$, $y$, $z$, $p_{dos}$ are swept. (b) Consensus calibration: $P_{secure}$ as $\eta$ and $\beta$ are swept from 0.05 to 0.25. (c) Whether relative protocol rankings change. |
| **Inputs** | Sweep ranges: $x \in [0.90, 0.999]$, $y \in [0.01, 0.20]$, $z \in [0.05, 0.45]$, $p_{dos} \in [0.05, 0.50]$, $\eta \in [0.05, 0.25]$, $\beta \in [0.05, 0.25]$ |
| **Outputs** | Per-sweep: $P_{Compromise}^{IDS}$, $P_{Compromise}^{BFT}$, gain ratio, protocol ranking stability indicator (boolean: rankings unchanged?) |
| **Independent variables** | Swept parameter (one at a time) |
| **Dependent variables** | $P_{Compromise}$, relative protocol ranking |
| **Controlled variables** | All other parameters held at baseline when sweeping one |
| **Statistical tests** | One-at-a-time (OAT) parameter sweeps with 50 sample points per sweep. Ranking stability assessed by Kendall's tau correlation. |
| **Existing code** | `probabilistic_model.py`: `p_compromise_no_bc_12attack()`, `p_compromise_bc_12attack()`, `sensitivity_ranking()` |
| **Figures** | Figure 9 (Sensitivity spider/tornado), Figure 10 ($\eta$ sweep table plot), Figure 11 ($\beta$ sweep table plot) |
| **Tables** | Table IX ($\eta$ sensitivity), Table X ($\beta$ sensitivity) |
| **Inherited / Adapted / New** | **Inherited**: Sensitivity framework from prior work. **New**: IDS baseline sweep is new contribution. |
| **Expected interpretation** | Placeholder. Robustness verdict to be stated after sweeps are complete. |

---

## Experiment E6: Monte Carlo Validation

| Field | Specification |
|-------|---------------|
| **Research Question** | Validates E1, E2, E3 |
| **Hypothesis** | All analytical predictions agree with Monte Carlo estimates within 1% relative error. |
| **Objective** | Validate analytical closed-form expressions against stochastic simulation. |
| **What exactly are we measuring?** | For 6 key metrics: analytical value, Monte Carlo mean ($10^6$ trials), absolute error, relative error (%). |
| **Inputs** | $x = 0.95$, $m = 10$, $y = 0.05$, $z = 0.15$, $n = 51$, $f = 16$, $p_c = 0.05$, $10^6$ trials |
| **Outputs** | 6-row validation table: metric, analytical, MC mean, MC std, relative error |
| **Independent variables** | None (single-point validation) |
| **Dependent variables** | MC-estimated probabilities |
| **Controlled variables** | All parameters fixed at baseline |
| **Statistical tests** | 95% confidence intervals for MC estimates. Relative error threshold: 1%. |
| **Existing code** | Will require new MC simulation script (building on existing `verify_paper_values.py`). The analytical functions exist in `probabilistic_model.py`. |
| **Figures** | Figure 12 (MC convergence plot) |
| **Tables** | Table XI (MC Validation) |
| **Inherited / Adapted / New** | **Inherited**: MC framework from prior work. **Adapted**: Extended to validate IDS-vs-BFT specific metrics. |
| **Expected interpretation** | Placeholder. Agreement threshold to be assessed after simulation. |

---

## Experiment E7: Per-Protocol 12-Attack Security Evaluation

| Field | Specification |
|-------|---------------|
| **Research Question** | RQ2 |
| **Hypothesis** | H2 (extended: per-attack protocol differentiation) |
| **Objective** | Evaluate how each of the 9 consensus protocols affects each of the 12 attack probabilities individually, using consensus-dependent formulations. |
| **What exactly are we measuring?** | For each protocol × attack pair: $P_j^{Algo}$ using consensus-dependent formulas (committee size, voting phases, message complexity, latency, credit weight, VRF). |
| **Inputs** | Per-protocol parameters from `protocols.json`: $n_{val}$, $N_{phases}$, $M_c$, $L$, credit flag, VRF flag. Calibration: $\eta = 0.15$, $\beta = 0.10$, $\omega_{credit} = 0.40$, $\tau_{dos} = 1.0$ s, $\tau_{recv} = 2.0$ s, $\tau_{scada} = 5.0$ s. |
| **Outputs** | $9 \times 12$ matrix of attack probabilities. Per-protocol $P_{Compromise}$ and $P_{secure}$. Best protocol per attack vector. |
| **Independent variables** | Protocol (9 levels), Attack (12 levels) |
| **Dependent variables** | $P_j^{Algo}$, $P_{Compromise}^{Algo}$, $P_{secure}^{Algo}$ |
| **Controlled variables** | $x = 0.95$, $m = 10$, $p_c = 0.05$, $y = 0.05$ |
| **Statistical tests** | Analytical computation. Rankings validated via Kendall's tau under E5 parameter sweeps. |
| **Existing code** | `intrusion_detection_bft_paper.tex` Section 5.5 (formulas). New code needed to compute the full $9 \times 12$ matrix programmatically. |
| **Figures** | Figure 6 (Protocol comparison heatmap) |
| **Tables** | Table VII (Consensus-Dependent Joint Security — the $9 \times 14$ table) |
| **Inherited / Adapted / New** | **Inherited**: Consensus-dependent formulations from prior BFT comparison paper. **New**: Explicit identification of what is inherited vs. adapted must be stated. |
| **Expected interpretation** | Placeholder. Best protocol per attack and overall to be determined after computation. |

---

## Experiment E8: Consensus Feature Ablation

| Field | Specification |
|-------|---------------|
| **Research Question** | RQ2 (mechanism contribution) |
| **Hypothesis** | Each feature (credit evaluation, VRF, latency scaling) independently contributes to security. |
| **Objective** | Isolate the individual security contribution of credit-evaluation, VRF proposer blinding, and finality latency scaling by disabling each feature independently. |
| **What exactly are we measuring?** | $P_{secure}$ under four conditions: Normal, No Credit ($\omega_{credit} = 0$), No VRF ($p_{r,eff} = P_R$), No Latency ($L \to \infty$). Delta from normal for each. |
| **Inputs** | Three protocols: Classic PBFT (baseline), Tower BFT, RVR. Four conditions each. |
| **Outputs** | $3 \times 4$ ablation matrix. Per-attack probability changes under each ablation. |
| **Independent variables** | Feature ablation condition (4 levels) |
| **Dependent variables** | $P_{secure}$, per-attack probabilities for Sybil/Byz, Key, Receiver |
| **Controlled variables** | All other parameters fixed at baseline |
| **Statistical tests** | Deterministic analytical comparison. |
| **Existing code** | Existing ablation logic in `intrusion_detection_bft_paper.tex` Section 6.4. Code needed to reproduce programmatically. |
| **Figures** | None (table only) |
| **Tables** | Table XII (Ablation Study) |
| **Inherited / Adapted / New** | **Inherited**: Ablation design from prior work. Results reused if assumptions unchanged. |
| **Expected interpretation** | Placeholder. |

---

## Experiment E9: Computational Overhead Comparison

| Field | Specification |
|-------|---------------|
| **Research Question** | Supplementary (feasibility for resource-constrained meters) |
| **Hypothesis** | Pipelined BFT protocols ($\mathcal{O}(n)$) are computationally feasible for smart meter hardware. |
| **Objective** | Compare the computational requirements of IDS (SVM training + TFPG matching) vs. BFT consensus (hashing + signing + consensus messages) at the component level. |
| **What exactly are we measuring?** | Per-protocol: message count, message complexity class, communication overhead (msgs/tx). IDS: estimated FLOPS for SVM inference and Wagner-Fischer edit distance. |
| **Inputs** | Protocol parameters from `protocols.json`. IDS parameters from published paper (SVM kernel dimension, TFPG dictionary size). |
| **Outputs** | Comparative table of computational requirements by paradigm. |
| **Independent variables** | Defense paradigm (IDS vs. BFT), Protocol (for BFT) |
| **Dependent variables** | Message count, complexity class, computational cost estimate |
| **Controlled variables** | $n = 51$ nodes, fixed network topology |
| **Statistical tests** | Asymptotic complexity analysis (Big-O). No stochastic element. |
| **Existing code** | `probabilistic_model.py`: `om_message_count()`, `tbft_message_count()`. `protocols.json` for message counts. |
| **Figures** | Figure 13 (Message complexity comparison bar chart) |
| **Tables** | Table XIII (Computational Overhead), Table XIV (Message Complexity) |
| **Inherited / Adapted / New** | **Inherited**: Protocol message counts. **New**: IDS computational cost estimation and side-by-side comparison. |
| **Expected interpretation** | Placeholder. |

---

## Summary: Experiment → Output Mapping

| Experiment | RQ | Hypothesis | Primary Table | Primary Figure |
|-----------|-----|-----------|--------------|---------------|
| E1: Sheikh Benchmark | RQ1 | H1 | Table III | Figure 3 |
| E2: 12-Attack Coverage | RQ1 | H5 | Table IV, V | Figure 5 |
| E3: SPOF Analysis | RQ4 | H4 | Table VI | Figure 4 |
| E4: Temporal Window | RQ2 | H2 | Table VIII | Figure 7, 8 |
| E5: Sensitivity | RQ3 | H3 | Table IX, X | Figure 9, 10, 11 |
| E6: Monte Carlo | Validates E1–E3 | Agreement <1% | Table XI | Figure 12 |
| E7: Per-Protocol 12-Attack | RQ2 | H2 (ext.) | Table VII | Figure 6 |
| E8: Ablation | RQ2 | Feature contrib. | Table XII | — |
| E9: Computational Overhead | Supplementary | Feasibility | Table XIII, XIV | Figure 13 |
