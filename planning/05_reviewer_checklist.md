# Reviewer Checklist
## Anticipated Reviewer Questions and Pre-Built Answers

> For every likely reviewer question, trace the answer to a specific experiment, figure, or section.
> If a question cannot be answered, it becomes a research gap to address before submission.

---

## Category 1: Motivation & Significance

| # | Reviewer Asks | Points To | Section | Experiment | Figure/Table | Fully Answered? |
|---|--------------|-----------|---------|-----------|-------------|-----------------|
| Q1 | "Why compare IDS and blockchain? They solve different problems." | The SPOF argument: both aim to secure AMI, but IDS is reactive with SPOF, blockchain is proactive and distributed. | Sec. I-B, Sec. I-C | — | — | ✓ Addressed in Introduction |
| Q2 | "What specific gap in the literature does this fill?" | No prior work provides a formal quantitative comparison of IDS vs. blockchain under identical threat models. | Sec. II-C | — | Table I (Gap Analysis) | ✓ Gap table exists |
| Q3 | "Is the IDS paper a strawman? You're comparing against a 2022 paper." | We compare against the *architecture* (centralized SVM+TFPG), not against a specific classification accuracy. The architectural limitations (SPOF, reactive paradigm) apply to the entire class of centralized IDS approaches. | Sec. IV, Sec. IV-C | — | — | ✓ Must be explicit |
| Q4 | "Why not improve the IDS instead of replacing it?" | Future work proposes a hybrid IDS-Blockchain approach. The paper establishes the quantitative justification for the transition first. | Sec. XI-B (Future Work) | — | — | ✓ Hybrid mentioned |

---

## Category 2: Technical Validity

| # | Reviewer Asks | Points To | Section | Experiment | Figure/Table | Fully Answered? |
|---|--------------|-----------|---------|-----------|-------------|-----------------|
| Q5 | "Why $m = 10$ instead of $n_{sen} = 3854$?" | Sensor count dominance critique: $x^{3854}$ underflows to zero, making the model insensitive. Localized critical subset $m = 10$ represents realistic attacker behavior (targeting feeder heads). | Sec. III-D | E5 ($x$ sweep) | — | ✓ Justified |
| Q6 | "Why are attack probabilities assumed independent (Assumption A1)?" | Standard parallel failure model. Independence is a conservative upper bound. Bayesian correlated model (Sec. VI-B, future work) addresses this limitation. | Sec. X-A | — | — | ✓ Addressed in validity |
| Q7 | "Where do baseline probability values ($y = 0.05$, $z = 0.15$, etc.) come from?" | Each parameter cites a specific published source. All are subjected to sensitivity sweeps in E5. | Sec. III-C, Table I | E5 | Table I, Fig. 9 | ✓ Cited + swept |
| Q8 | "How do you justify the Poisson attack arrival assumption?" | Standard memoryless arrival model for independent cyber events. Sensitivity to $\lambda$ is swept in E5. | Sec. VI-B | E5 ($\lambda$ sweep) | — | ✓ Cited + swept |
| Q9 | "Why is $P_{Replay}^{BC} = 0$? No system achieves perfect security." | Blockchain nonces and cryptographic block sequencing make exact replay structurally impossible (replayed transactions have stale nonces/timestamps). This is a property of the protocol, not an empirical estimate. | Sec. V-B | E2 | Table V | ✓ Structural argument |
| Q10 | "Your Monte Carlo only validates your analytical formulas, not the underlying physical model." | Acknowledged as Construct Validity limitation. MC validates mathematical correctness of formulas, not the accuracy of baseline parameters. | Sec. X-C | E6 | Table XI | ✓ Acknowledged |

---

## Category 3: Comparison Fairness

| # | Reviewer Asks | Points To | Section | Experiment | Figure/Table | Fully Answered? |
|---|--------------|-----------|---------|-----------|-------------|-----------------|
| Q11 | "The IDS paper uses physical testbeds (SBCs + NS-3). Your work is purely analytical. Is this a fair comparison?" | We compare *architectures* and *paradigms*, not experimental setups. The IDS's physical validation does not change its centralized SPOF. Future Paper 3 will provide empirical blockchain benchmarks (Hyperledger + NS-3). | Sec. X-B, Sec. XI-B | — | — | ⚠️ Partially — must acknowledge explicitly |
| Q12 | "You claim 170 OoM improvement but that's the Sheikh model, not your contribution." | Correctly identified as inherited (C3). This paper's novel contributions are the paradigm comparison (C1) and SPOF quantification (C2). The 170 OoM figure is the *benchmark*, not the *contribution*. | Sec. I-C, Sec. VI-A | E1 | Table III | ✓ Must tag as inherited |
| Q13 | "The computational overhead of BFT consensus may make it impractical on resource-constrained meters." | Addressed in E9. Pipelined protocols ($\mathcal{O}(n)$) have comparable overhead to SVM inference. Full empirical validation deferred to Paper 3. | Sec. VII-E | E9 | Table XIII, XIV | ⚠️ Partially — analytical only |
| Q14 | "You compare 9 protocols but only 2 are truly sub-second (Tower BFT, RVR). Is that enough?" | These represent the state-of-the-art in pipelined BFT. The 9-protocol span covers the full evolutionary landscape (G1-G4), providing context for why sub-second protocols emerged. | Sec. VIII | E4 | Table VIII | ✓ Context provided |

---

## Category 4: Novelty

| # | Reviewer Asks | Points To | Section | Experiment | Figure/Table | Fully Answered? |
|---|--------------|-----------|---------|-----------|-------------|-----------------|
| Q15 | "What is actually new here? Most of the mathematical framework seems to come from prior work." | Two novel contributions: (C1) first formal paradigm comparison framework (IDS vs BFT under identical threat model), (C2) first quantitative SPOF vulnerability comparison. Everything else is explicitly tagged as inherited/adapted. | Contribution Mapping, Sec. I-C | E2, E3 | Table I (Gap), Table IV, V, VI | ✓ If tagging is explicit |
| Q16 | "Is the paradigm comparison (reactive vs. proactive) an obvious observation that doesn't need a paper?" | The observation is intuitive, but no prior work has *quantified* the advantage across 12 attack vectors with Monte Carlo validation. The paper converts an intuition into a mathematical proof. | Sec. I-C, Sec. VII | E1, E2, E6 | Tables III-VI | ✓ Quantification is the contribution |
| Q17 | "Why not compare against other defense paradigms (e.g., Moving Target Defense, Zero Trust)?" | Scope limitation: this paper compares the two most prevalent paradigms in AMI literature (IDS and blockchain). Extension to MTD/Zero Trust is future work. | Sec. X-B | — | — | ✓ Scope bounded |

---

## Category 5: Consensus Protocol Selection

| # | Reviewer Asks | Points To | Section | Experiment | Figure/Table | Fully Answered? |
|---|--------------|-----------|---------|-----------|-------------|-----------------|
| Q18 | "Why PBFT and not Raft, Paxos, or Proof-of-Stake?" | PBFT family provides Byzantine fault tolerance (BFT), which is required for adversarial environments. Raft/Paxos assume crash faults only. PoS is for permissionless chains. AMI requires permissioned BFT. | Sec. V-C, Sec. II-B | — | — | ✓ Justified |
| Q19 | "Tower BFT is Solana's protocol. Isn't it designed for financial transactions, not smart grids?" | Tower BFT's technical properties (sub-second finality, $\mathcal{O}(n)$ messages, PoH ordering) are architecture-agnostic. We evaluate it for smart grid suitability based on these properties. | Sec. VIII | E4 | Table VIII | ✓ Property-based evaluation |
| Q20 | "Protocol latency numbers come from different papers with different testbeds. How comparable are they?" | Acknowledged as Conclusion Validity limitation (Sec. X-D). Mitigated by using normalized relative factors, not absolute numbers. Paper 3 will provide unified benchmarks. | Sec. X-D | — | — | ✓ Acknowledged |

---

## Category 6: Reproducibility

| # | Reviewer Asks | Points To | Section | Experiment | Figure/Table | Fully Answered? |
|---|--------------|-----------|---------|-----------|-------------|-----------------|
| Q21 | "Can I reproduce your results?" | Yes: `probabilistic_model.py` (849 lines) contains all analytical functions. `protocols.json` contains all protocol parameters. Running `python probabilistic_model.py` executes all verifications. | — | All | — | ✓ Code available |
| Q22 | "Are your figures generated from the same code as your numerical claims?" | Yes: all figures in `figures/` are generated programmatically from `probabilistic_model.py` outputs. | — | All | All | ✓ Code-generated |

---

## Category 7: Impact & Practical Implications

| # | Reviewer Asks | Points To | Section | Experiment | Figure/Table | Fully Answered? |
|---|--------------|-----------|---------|-----------|-------------|-----------------|
| Q23 | "What should a utility operator do based on this paper?" | Deploy permissioned BFT blockchain with Tower BFT or RVR consensus for high-security AMI; use CE-PBFT or SV-PBFT for high-throughput microgrids. Consensus selection roadmap in Sec. VIII-B. | Sec. VIII-B | E4 | Table VIII | ✓ Actionable |
| Q24 | "Is there a transition path from IDS to blockchain, or does this require rip-and-replace?" | Future work (Sec. XI-B) proposes hybrid IDS-Blockchain where lightweight SVM pre-filter reduces consensus load. This paper establishes *why* the transition is justified. | Sec. XI-B | — | — | ✓ Hybrid path noted |

---

## Unresolved Questions (Gaps to Address Before Submission)

| # | Question | Status | Mitigation |
|---|---------|--------|-----------|
| G1 | The IDS paper's actual detection accuracy numbers are not reproduced — only architectural limitations are critiqued. | ⚠️ Gap | Add paragraph acknowledging IDS detection accuracy is high but does not address SPOF. |
| G2 | No empirical blockchain deployment on smart meter hardware. | ⚠️ Gap | Explicitly deferred to Paper 3. Acknowledged in Sec. X-B. |
| G3 | Consensus-dependent formulas ($P_j^{Algo}$) involve calibration parameters ($\eta$, $\beta$) that are not empirically validated. | ⚠️ Gap | Sensitivity sweeps (E5) show results are robust to calibration values. Acknowledged in Sec. X-C. |
| G4 | The $P_{Replay} = 0$ claim assumes no implementation bugs in nonce handling. | Minor | Add footnote: "assuming correct protocol implementation." |

---

## Summary Statistics

| Category | Questions | Fully Answered | Partially | Unresolved |
|---------|-----------|:-:|:-:|:-:|
| Motivation | 4 | 4 | 0 | 0 |
| Technical Validity | 6 | 6 | 0 | 0 |
| Comparison Fairness | 4 | 2 | 2 | 0 |
| Novelty | 3 | 3 | 0 | 0 |
| Consensus Selection | 3 | 3 | 0 | 0 |
| Reproducibility | 2 | 2 | 0 | 0 |
| Impact | 2 | 2 | 0 | 0 |
| **Total** | **24** | **22** | **2** | **0** |
| **Gaps** | **4** | — | — | — |
