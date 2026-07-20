# Mathematical Notation Dictionary
## IDS → BFT Blockchain Comparative Paper

> Every symbol, assumption, and equation is standardized here.
> The paper must use identical notation throughout.

---

## System Parameters

| Symbol | Meaning | Type | Units | Domain | First Appears | Notes |
|--------|---------|------|-------|--------|---------------|-------|
| $n$ | Total number of validator/participant nodes | Positive integer | nodes | $n \geq 4$ | Eq. (1), Sec. III | IEEE 33-bus + 50 EVs = 51 |
| $n_{sen}$ | Total number of sensors in the system | Positive integer | sensors | $n_{sen} > 0$ | Eq. (1), Sec. III | $n_{sen}^{DN} + n_{sen}^{EV} = 3854$ |
| $n_{sen}^{DN}$ | Sensors in Distribution Network | Positive integer | sensors | — | Eq. (1), Sec. III | $33 + 32 + 64 = 129$ |
| $n_{sen}^{EV}$ | Sensors in EV parking lot | Positive integer | sensors | — | Eq. (1), Sec. III | $50 + 1225 + 2450 = 3725$ |
| $f$ | Byzantine fault tolerance limit | Non-negative integer | nodes | $f = \lfloor(n-1)/3\rfloor$ | Sec. III | $f = 16$ for $n = 51$ |
| $m$ | Critical sensor subset size | Positive integer | sensors | $m \ll n_{sen}$ | Eq. (2), Sec. III-D | $m = 10$ (localized attack model) |
| $k_1$ | Number of P2P communication links in local mesh | Positive integer | links | $k_1 = m(m-1)/2$ | Eq. (8) | $k_1 = 45$ |
| $k_2$ | Number of receiver nodes requiring compromise | Non-negative integer | nodes | $k_2 = \lfloor m \times 0.33 \rfloor$ | Eq. (16) | $k_2 = 3$ |

---

## Attack Probability Parameters (Baseline — Without Blockchain)

| Symbol | Meaning | Type | Units | Baseline Value | Range (Sensitivity) | Source |
|--------|---------|------|-------|----------------|---------------------|--------|
| $x$ | Per-sensor security level | Real | probability | 0.95 | $[0.90, 0.999]$ | Sheikh et al. 2020 |
| $y$ | MitM session vulnerability | Real | probability | 0.05 | $[0.01, 0.20]$ | Baumeister 2010 |
| $z$ | Replay attack success rate | Real | probability | 0.15 | $[0.05, 0.45]$ | Yan et al. 2012 |
| $p_{dos}$ | Single-node DoS flooding probability | Real | probability | 0.20 | $[0.05, 0.50]$ | Wang & Lu 2013 |
| $p_{ddos}$ | Botnet DDoS saturation probability | Real | probability | 0.35 | $[0.10, 0.60]$ | Wang & Lu 2013 |
| $p_{key}$ | Key compromise probability | Real | probability | 0.01 | $[0.001, 0.05]$ | Sridhar et al. 2012 |
| $P_{SCADA}$ | SCADA system compromise probability | Real | probability | 0.01 | $[0.01, 0.05]$ | Sheikh et al. 2020 |
| $P_R$ | Receiver/actuator override probability | Real | probability | 0.01 | $[0.01, 0.05]$ | Sheikh et al. 2020 |
| $p_c$ | Per-validator compromise probability | Real | probability | 0.05 | $[0.01, 0.20]$ | Li et al. 2020 |

---

## Consensus Calibration Parameters

| Symbol | Meaning | Type | Units | Baseline Value | Rationale |
|--------|---------|------|-------|----------------|-----------|
| $\eta$ | Spatial cross-verification factor | Real | dimensionless | 0.15 | Validator redundancy coefficient: spatial cross-validation reduces tamper success by up to 15% for large committees |
| $\beta$ | Per-phase verification factor | Real | dimensionless | 0.10 | Multi-round verification gain: each voting phase filters independent Byzantine deviations by 10% |
| $\omega_{credit}$ | Credit system efficiency | Real | dimensionless | 0.40 | Historical reputation filters compromise likelihood by 40% |
| $\tau_{dos}$ | DoS saturation time constant | Real | seconds | 1.0 | Typical flooding saturation threshold of local network interfaces |
| $\tau_{recv}$ | Receiver override window | Real | seconds | 2.0 | Safety margin of local actuators under unfinalized commands |
| $\tau_{scada}$ | SCADA command validation window | Real | seconds | 5.0 | Delay within which central operator checks mismatch |

---

## Protocol Parameters (Per-Consensus Algorithm)

| Symbol | Meaning | Type | Units |
|--------|---------|------|-------|
| $n_{val}$ | Committee/validator size for this protocol | Positive integer | nodes |
| $N_{phases}$ | Number of explicit voting phases | Positive integer | phases |
| $M_c$ | Total message count for consensus round | Positive integer | messages |
| $L$ | Consensus latency (finality time) | Real | milliseconds |
| $\sigma_{CO}^{Algo}$ | Log-normalized communication overhead | Real | dimensionless |

---

## 12 Attack Probability Symbols — Without Blockchain (Centralized IDS)

| Symbol | Attack Type | Formula | Baseline Value |
|--------|-----------|---------|----------------|
| $P_{SA}$ | Sensor Compromise | $x^m$ | $0.95^{10} \approx 0.599$ |
| $P_{FDI}$ | False Data Injection | $x^m$ | $0.599$ |
| $P_{CA}$ | Communication Compromise | $x^m$ | $0.599$ |
| $P_{MitM}$ | Man-in-the-Middle | $y$ | $0.05$ |
| $P_{Replay}$ | Replay Attack | $z$ | $0.15$ |
| $P_{Sybil}$ | Sybil Attack | $1.0$ | $1.0$ (open network) |
| $P_{DoS}$ | Denial of Service | $p_{dos}$ | $0.20$ |
| $P_{DDoS}$ | Distributed DoS | $p_{ddos}$ | $0.35$ |
| $P_{Byz}$ | Byzantine Validator | $1.0$ | $1.0$ (SPOF) |
| $P_{Key}$ | Key Compromise | $p_{key}$ | $0.01$ |
| $P_{SCADA}$ | SCADA Breach | $0.01$ | $0.01$ |
| $P_R$ | Receiver Override | $0.01$ | $0.01$ |

---

## 12 Attack Probability Symbols — With Blockchain (BFT Consensus)

| Symbol | Attack Type | Formula | Model Type |
|--------|-----------|---------|------------|
| $P_{SA}^{BC}$ | Sensor Compromise | $x^{2m}$ | Proposed |
| $P_{FDI}^{BC}$ | False Data Injection | $x^{2m}$ | Proposed |
| $P_{CA}^{BC}$ | Communication Compromise | $x^{2k_1}$ | Proposed |
| $P_{MitM}^{BC}$ | Man-in-the-Middle | $y^2$ | Proposed |
| $P_{Replay}^{BC}$ | Replay Attack | $0.0$ | Adopted (nonces) |
| $P_{Sybil}^{BC}$ | Sybil Attack | $\sum_{i=f+1}^{n} \binom{n}{i} p_c^i (1-p_c)^{n-i}$ | Adopted (BFT) |
| $P_{DoS}^{BC}$ | Denial of Service | $p_{dos} \cdot \frac{f+1}{n}$ | Modified |
| $P_{DDoS}^{BC}$ | Distributed DoS | $p_{ddos} \cdot \frac{f+1}{n}$ | Modified |
| $P_{Byz}^{BC}$ | Byzantine Validator | $\sum_{i=f+1}^{n} \binom{n}{i} p_c^i (1-p_c)^{n-i}$ | Adopted (BFT) |
| $P_{Key}^{BC}$ | Key Compromise | $P_{R,shamir}(3,5)$ | Adopted (Shamir) |
| $P_{SCADA}^{BC}$ | SCADA Breach | $(P_{SCADA} \cdot x)^m$ | Proposed |
| $P_R^{BC}$ | Receiver Override | $P_R^{k_2} \cdot x^m$ | Proposed |

---

## Consensus-Dependent Attack Symbols (Per-Algorithm)

| Symbol | Formula | Dependency |
|--------|---------|-----------|
| $P_{Sensor}^{Algo}$ | $x^{2m} \cdot (1 - \eta \cdot n_{val}/n_{global})$ | Committee size |
| $P_{FDI}^{Algo}$ | $x^{2m} \cdot (1 - \beta \cdot N_{phases})$ | Voting phases |
| $P_{Comm}^{Algo}$ | $x^{2k_1} \cdot \sigma_{CO}^{Algo}$ | Message complexity |
| $P_{MitM}^{Algo}$ | $y^2 / n_{val}$ | Committee size |
| $P_{DoS}^{Algo}$ | $p_{dos} \cdot \frac{f+1}{n_{val}} \cdot \sigma_{CO}^{Algo} \cdot (1 - e^{-L/\tau_{dos}})$ | Latency, msg. complexity |
| $P_{DDoS}^{Algo}$ | $p_{ddos} \cdot \frac{f+1}{n_{val}} \cdot \sigma_{CO}^{Algo} \cdot (1 - e^{-L/\tau_{dos}})$ | Latency, msg. complexity |
| $P_{Sybil}^{Algo}$ | Binomial tail with $p_{c,eff}$ | Credit system |
| $P_{Byz}^{Algo}$ | Binomial tail with $p_{c,eff}$ | Credit system |
| $P_{Key}^{Algo}$ | $P_{R,shamir}(3, 5, p_{r,eff\_key})$ | Credit system |
| $P_{SCADA}^{Algo}$ | $(P_{SCADA} \cdot x)^m \cdot p_{c,eff} \cdot (1 - e^{-L/\tau_{scada}})$ | Latency, credit |
| $P_{Receiver}^{Algo}$ | $(p_{r,eff\_recv})^{k_2} \cdot x^m \cdot (1 - e^{-L/\tau_{recv}})$ | Latency, VRF |

Where:
- $p_{c,eff} = p_c(1 - \omega_{credit})$ for credit-evaluated protocols; $p_c$ otherwise
- $p_{r,eff\_key} = P_R(1 - \omega_{credit})$ for credit-evaluated; $P_R$ otherwise
- $p_{r,eff\_recv} = P_R / n_{val}$ for VRF-enabled (RVR); $P_R$ otherwise
- $\sigma_{CO}^{Algo} = \log_{10}(M_c^{Algo}) / \log_{10}(M_{c,OM(m)})$

---

## Aggregate Security Metrics

| Symbol | Meaning | Formula | Appears In |
|--------|---------|---------|-----------|
| $P_{Compromise}^{IDS}$ | System compromise probability (centralized IDS) | $1 - \prod_{j=1}^{12}(1 - P_{atk}^j)$ | E2, Sec. VI |
| $P_{Compromise}^{BFT}$ | System compromise probability (BFT blockchain) | $1 - \prod_{j=1}^{12}(1 - P_{atk}^{BC,j})$ | E2, Sec. VI |
| $P_{secure}^{IDS}$ | System security (centralized IDS) | $1 - P_{Compromise}^{IDS}$ | E2, Sec. VI |
| $P_{secure}^{BFT}$ | System security (BFT blockchain) | $1 - P_{Compromise}^{BFT}$ | E2, Sec. VI |
| $P_{TA}$ | Sheikh target attack probability (no BC) | $\frac{1}{4}(2x^{n_{sen}} + P_{SCADA} + P_R)$ | E1, Sec. VI-A |
| $P_{TAb}$ | Sheikh target attack probability (with BC) | $\frac{1}{4}(P_{SAb} + P_{CAb} + P_{SCADAb} + P_{Rb})$ | E1, Sec. VI-A |

---

## Temporal Security Metrics

| Symbol | Meaning | Formula | Appears In |
|--------|---------|---------|-----------|
| $\lambda$ | Attack arrival rate | — | attacks/second | E4, Sec. VI-B |
| $L$ | Consensus latency | — | milliseconds | E4, Sec. VI-B |
| $P_{temporal}$ | Temporal vulnerability probability | $1 - e^{-\lambda \cdot L \cdot P_{TA}}$ | E4, Sec. VI-B |
| $P_{secure}$ | Overall security probability | $(1 - P_{TAb})(1 - P_{temporal})(1 - P_{other})$ | E4, Sec. VI-B |
| $P_{other}$ | Residual risk | Constant | 0.05 | E4, Sec. VI-B |
| $\rho$ | Attack correlation coefficient | Constant | 0.3 | E4, Sec. VI-B |

---

## Key Management Symbols

| Symbol | Meaning | Formula |
|--------|---------|---------|
| $P_{R,shamir}(k,d)$ | Shamir $(k,d)$ threshold compromise | $\sum_{i=k}^{d} \binom{d}{i} P_{share}^i (1-P_{share})^{d-i}$ |
| $P_{R,MPC}(k,n)$ | MPC threshold compromise | $0.7 \cdot P_{R,shamir}(k,n)$ |
| $P_{R,multisig}(k,n)$ | Multisig threshold compromise | $0.85 \cdot P_{R,shamir}(k,n)$ |
| $P_{share}$ | Per-share compromise probability | 0.01 |

---

## IDS-Specific Symbols (From Target Paper)

| Symbol | Meaning | Notes |
|--------|---------|-------|
| $ADS_{ind}$ | Anomaly Detection System indicator | $\{0, 1\}$; set to 1 when SVM flags anomaly |
| $IDS_{ind}$ | Intrusion Detection similarity index | Real $\in [0, 1]$; compared to threshold |
| $K(x_i, x_j)$ | SVM kernel function | RBF: $\exp(-\gamma\|x_i - x_j\|^2)$ |
| $d(i, j)$ | Wagner-Fischer edit distance | Integer; between observed and reference sequences |
| TFPG | Temporal Failure Propagation Graph | Predefined attack signature paths |

---

## Assumptions Register

| ID | Assumption | Justification | Where Validated |
|----|-----------|---------------|-----------------|
| A1 | Attack independence: 12 vectors act as independent parallel failure modes | Standard series reliability model; conservative upper-bound | E5 sensitivity, Sec. X-A |
| A2 | Localized critical subset $m = 10$ instead of global $n_{sen} = 3854$ | Attacker targets feeder heads; global exponent underflows | Sec. III-D |
| A3 | Per-sensor security $x = 0.95$ represents standard hardware without tamper-resistant modules | Aligned with Sheikh et al. baseline | E5 sensitivity sweep |
| A4 | Poisson attack arrivals with rate $\lambda$ | Standard memoryless arrival process for cyber attacks | Sec. VI-B |
| A5 | BFT fault tolerance holds for $f \leq \lfloor(n-1)/3\rfloor$ | Lamport et al. 1982 proven bound | Theorem 1 |
| A6 | IDS has centralized MDMS as single coordinator | Architecture from target paper | Sec. IV |
| A7 | Blockchain replays eliminated by nonces and timestamps | Standard blockchain property | Sec. V-B |
| A8 | Credit evaluation reduces effective $p_c$ by factor $(1 - \omega_{credit})$ | CE-PBFT, SV-PBFT design feature | Sec. VI-B |
| A9 | VRF proposer hiding reduces receiver override to $P_R / n_{val}$ | RVR design feature | Sec. VI-B |
