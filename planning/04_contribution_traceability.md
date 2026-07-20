# Contribution Traceability Matrix + Paper Dependency Graph + Publication Strategy
## IDS → BFT Blockchain Comparative Paper

---

## Part A: Contribution Traceability Matrix

> Every claimed contribution must map to actual evidence.
> If a contribution cannot point to an experiment, figure, or section — it is not a contribution.

| # | Claimed Contribution | Evidence Type | Evidence Location | Inherited / Adapted / New |
|---|---------------------|--------------|-------------------|---------------------------|
| C1 | **Paradigm Comparison Framework**: First formal quantitative comparison of reactive IDS vs. proactive BFT consensus for AMI under identical threat model | Framework + Evaluation | **Section VII** (Comparative Evaluation), **Table IV** (Coverage Matrix), **Table V** (Attack-by-Attack), **Experiment E2** | **NEW** — No prior work compares IDS and blockchain under identical 12-attack model |
| C2 | **SPOF Vulnerability Quantification**: Formal proof that centralized IDS has $P_{Byz} = 1.0$ while BFT has $P_{Byz} \approx 10^{-10}$ | Analytical proof + Figure | **Section VII-B**, **Experiment E3**, **Figure 4**, **Table VI** | **NEW** — SPOF comparison not in any prior work |
| C3 | **170 OoM Static Security Gain** (Sheikh baseline reproduction): $P_{TA} \approx 0.005 \to P_{TAb} \approx 10^{-173}$ | Analytical reproduction | **Section VI-A**, **Experiment E1**, **Figure 3**, **Table III** | **INHERITED** from Sheikh et al. 2020, reproduced without modification |
| C4 | **12-Attack Extension**: Extending 4-component model to 12 explicit cyber-physical attack vectors | Extended model | **Section III-C** (definitions), **Section VI** (evaluation), **Experiment E2**, **Table V** | **ADAPTED** from prior BFT comparison work; recontextualized as IDS comparison |
| C5 | **Sensor Count Dominance Critique**: Global $n_{sen} = 3854$ exponent underflows; localized $m = 10$ restores model sensitivity | Analytical critique | **Section III-D**, **Eq. (2)** | **INHERITED** from prior BFT comparison work; presented here as supporting evidence |
| C6 | **Temporal Security Model (STSF)**: Poisson-based temporal attack window analysis for consensus latency exposure | Temporal framework | **Section VI-B**, **Experiment E4**, **Figure 7**, **Figure 8**, **Table VIII** | **INHERITED** from prior STSF work; applied unchanged to IDS comparison context |
| C7 | **9-Protocol Consensus Evaluation**: Comparative evaluation of 9 BFT protocols across 4 groups for AMI deployment | Protocol comparison | **Section VIII**, **Experiment E4, E7**, **Table VII, VIII**, **Figure 6, 7** | **INHERITED** from prior BFT comparison work; presented as AMI deployment guidance |
| C8 | **Monte Carlo Validation**: $10^6$-trial simulation confirming analytical accuracy within 0.5% | Simulation | **Section IX-C**, **Experiment E6**, **Table XI**, **Figure 12** | **INHERITED** from prior work; extended with IDS-specific metrics if needed |
| C9 | **Sensitivity & Robustness Analysis**: Parameter sweeps confirming comparative advantage across all operating ranges | Sensitivity study | **Section IX-B**, **Experiment E5**, **Table IX, X**, **Figure 9, 10, 11** | **ADAPTED** from prior work; extended with IDS baseline sweeps |
| C10 | **Ablation Study**: Feature contribution isolation for credit, VRF, and latency scaling | Ablation | **Section IX-D**, **Experiment E8**, **Table XII** | **INHERITED** from prior work |

### Inheritance Summary

| Category | Count | Contributions |
|----------|-------|--------------|
| **NEW** (original to this paper) | 2 | C1, C2 |
| **ADAPTED** (reused with modifications/reframing) | 2 | C4, C9 |
| **INHERITED** (reused unchanged, properly cited) | 6 | C3, C5, C6, C7, C8, C10 |

> [!IMPORTANT]
> **Reviewer-facing clarity**: The paper must explicitly state in Section I (Introduction, "Our Contributions" list) which elements are new to this work and which are inherited from prior publications. Inherited contributions must be cited. This prevents the appearance of claiming prior work as new.

---

## Part B: Paper Dependency Graph

> Instead of a linear section flow, this shows what logically depends on what.
> Everything is traceable from research questions to final discussion.

```
RQ1 (Is BFT > IDS statically?)
├── Threat Model (Sec. III-C: 12 attacks)
│   └── E2: 12-Attack Coverage Comparison
│       ├── Table IV (Coverage Matrix)
│       ├── Table V (Attack-by-Attack Quantitative)
│       ├── Figure 5 (Bar Chart)
│       └── Discussion: Sec. VII-A (Defense Paradigm), VII-C (Coverage)
├── Sheikh Baseline (Sec. VI-A)
│   └── E1: Sheikh 4-Component Benchmark
│       ├── Table III (Sheikh Reproduction)
│       ├── Figure 3 (P_TA vs x)
│       └── Discussion: Sec. VII-D (Quantification)
└── SPOF Analysis (Sec. VII-B)
    └── E3: SPOF Vulnerability
        ├── Table VI (SPOF Risk)
        ├── Figure 4 (P_Byz vs p_c)
        └── Discussion: Sec. VII-B

RQ2 (Which consensus protocol for AMI?)
├── Temporal Model (Sec. VI-B: Poisson)
│   └── E4: Temporal Vulnerability Window
│       ├── Table VIII (Protocol Ranking)
│       ├── Figure 7 (Latency vs P_secure)
│       ├── Figure 8 (P_temporal curve)
│       └── Discussion: Sec. VIII-A
├── Per-Protocol Evaluation (Sec. VIII)
│   └── E7: Per-Protocol 12-Attack
│       ├── Table VII (9×14 matrix)
│       ├── Figure 6 (Heatmap)
│       └── Discussion: Sec. VIII
├── Feature Contribution (Sec. IX-D)
│   └── E8: Ablation Study
│       ├── Table XII (Ablation)
│       └── Discussion: Sec. IX-D
└── Feasibility (Sec. VII-E)
    └── E9: Computational Overhead
        ├── Table XIII, XIV
        ├── Figure 13
        └── Discussion: Sec. VII-E

RQ3 (Is advantage robust?)
├── Parameter Sensitivity (Sec. IX-B)
│   └── E5: Sensitivity Analysis
│       ├── Table IX (η), Table X (β)
│       ├── Figure 9, 10, 11
│       └── Discussion: Sec. IX-B
└── Monte Carlo (Sec. IX-C)
    └── E6: Monte Carlo Validation
        ├── Table XI
        ├── Figure 12
        └── Discussion: Sec. IX-C

RQ4 (SPOF quantification)
└── (See RQ1 → SPOF Analysis above)
```

### Section Writing Order (Dependency-Aware)

The sections should be written in this order to avoid forward-referencing undefined concepts:

| Order | Section | Depends On |
|-------|---------|-----------|
| 1 | Math Dictionary | Nothing |
| 2 | Sec. III: System Architecture & Threat Model | Math Dictionary |
| 3 | Sec. IV: IDS Analysis | Sec. III (threat model) |
| 4 | Sec. V: BFT Framework | Sec. III (threat model) |
| 5 | Sec. VI-A: Static Security (Sheikh + 12-attack) | Sec. III, IV, V (both models defined) |
| 6 | Sec. VI-B: Temporal Security | Sec. VI-A (P_TA needed) |
| 7 | Sec. VII: Comparative Evaluation | Sec. VI (all security metrics) |
| 8 | Sec. VIII: Consensus Protocol Selection | Sec. VI-B (temporal model) |
| 9 | Sec. IX: Experimental Results | Sec. VI, VII, VIII (all models) |
| 10 | Sec. X: Threats to Validity | Sec. IX (results to qualify) |
| 11 | Sec. II: Related Work | All above (position paper in literature) |
| 12 | Sec. I: Introduction | All above (summarize contributions) |
| 13 | Abstract | Everything |
| 14 | Sec. XI: Conclusion | Everything |

> [!TIP]
> Write the Introduction and Abstract **last**. They summarize the entire paper, so they should reflect the final state of all other sections.

---

## Part C: Publication Strategy

> Don't think about one paper. Think about three.

### Paper Portfolio

| Paper | Title (Working) | Venue Target | Status | Key Contribution |
|-------|----------------|--------------|--------|-----------------|
| **Paper 1** | "From Reactive Detection to Proactive Consensus: A Comparative Static-Temporal Security Evaluation Framework for BFT Blockchain in AMI" | IEEE Access / SEGAN / Sustainable Computing | **THIS PAPER** | Paradigm comparison (IDS vs BFT), SPOF elimination proof, 12-attack comparative framework |
| **Paper 2** | "Static-Temporal Security Framework for Evaluating BFT Consensus Protocols in Smart Grid Energy Trading" | IEEE Transactions on Industrial Informatics | Existing work (reframe) | STSF methodology itself, temporal critique of Sheikh et al., 9-protocol evaluation |
| **Paper 3** | "Performance Benchmarking of Byzantine Fault Tolerant Consensus Algorithms for Permissioned Blockchain in Cyber-Physical Systems" | IEEE Transactions on Smart Grid | Future work | Hyperledger benchmarking, NS-3 simulation, empirical latency/throughput measurements |

### Citation Chain

```
Paper 3 cites Paper 2 (for STSF framework)
Paper 3 cites Paper 1 (for IDS comparison context)
Paper 2 cites Sheikh et al. 2020 (for baseline model)
Paper 1 cites Paper 2 (for STSF and consensus evaluation)
Paper 1 cites Sheikh et al. 2020 (for baseline model)
Paper 1 cites IDS smart meter paper (for target comparison)
```

### What Each Paper Claims as Original

| Contribution | Paper 1 Claims | Paper 2 Claims | Paper 3 Claims |
|-------------|:-:|:-:|:-:|
| Paradigm comparison (IDS vs BFT) | ✓ Original | — | — |
| SPOF vulnerability quantification | ✓ Original | — | — |
| 12-attack extension model | — | ✓ Original | — |
| Static-Temporal Security Framework | — | ✓ Original | — |
| Sensor count dominance critique | — | ✓ Original | — |
| 9-protocol comparative evaluation | — | ✓ Original | — |
| Monte Carlo validation | — | ✓ Original | — |
| Empirical Hyperledger benchmarks | — | — | ✓ Original |
| NS-3 network simulation | — | — | ✓ Original |
| Bayesian correlated attack models | — | — | ✓ Original |

> [!IMPORTANT]
> Paper 1 (this paper) has **two novel contributions**: (C1) the paradigm comparison framework and (C2) the SPOF vulnerability quantification. Everything else is inherited from Paper 2 or prior literature. The paper must be transparent about this.
