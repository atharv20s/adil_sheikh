# AMI-CPSD v1.0: Advanced Metering Infrastructure Cyber-Physical Synthetic Digital Twin Dataset

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Dataset: 1.1M Rows](https://img.shields.io/badge/Dataset-1.1M_Rows-green.svg)](#dataset-scale)
[![Target: IEEE Transactions](https://img.shields.io/badge/Target-IEEE_Transactions-orange.svg)](#citation)

**AMI-CPSD v1.0** is a research-grade, production-quality synthetic dataset generation framework designed for the benchmark paper:

> **"AI-Assisted Blockchain-Based Intrusion Detection for Advanced Metering Infrastructure (AMI)"**

Unlike primitive uniform random CSV generators, **AMI-CPSD v1.0** operates as a **physics-grounded Digital Twin** of a Smart Grid Advanced Metering Infrastructure (AMI) coupled with Byzantine Fault Tolerant (BFT) blockchain consensus networks.

---

## 🌟 Key Features & Digital Twin Architecture (19 Research-Grade Capabilities)

1. **Continuous Temporal Dynamics (AR(1) & Ornstein–Uhlenbeck Processes)**: State evolution over time ($t_0 \to t_1 \to t_2 \to \dots$) for Voltage, Current, Power, Energy, CPU, and Temperature.
2. **Hierarchical Grid Topology**: Real-world power network hierarchy ($\text{Substation} \to \text{Feeder} \to \text{Transformer} \to \text{NAN} \to \text{Smart Meter}$).
3. **Graph Neural Network (GNN) Support**: Exports spatial adjacency matrix, line impedance ($R + jX$), and communication graph (`metadata/topology_graph.json`) for GCN, GAT, and GraphSAGE models.
4. **Weather & Environmental Coupling**: `ambient_temperature`, `humidity`, `solar_irradiance`, `wind_speed`, `time_of_day`, `day_of_week`, `is_holiday` driving HVAC building loads.
5. **Sector Consumer Profiles**: Distinct load dynamics for **Residential**, **Commercial**, and **Industrial** consumers.
6. **Physics Validation Engine**: Enforces exact power flow constraints $|P_{\text{measured}} - (V \cdot I \cdot \cos\phi / 1000)| < \varepsilon$.
7. **5-Stage Sequential Attack Progression**: Stateful attack lifecycle progression ($\text{Reconnaissance} \to \text{Exploitation} \to \text{Escalation} \to \text{Impact} \to \text{Post-Attack}$).
8. **Explainability (XAI) Attribution Labels**: Ground-truth `affected_features` column listing exact perturbed feature subsets for SHAP/XAI attribution evaluation.
9. **Multi-Consensus BFT Engine**: Selectable BFT protocols: `PBFT`, `IBFT`, `QBFT`, `TowerBFT`, `RVR_BFT`.
10. **Attack Intensity Levels**: Injected attacks with variable intensity levels (`Low`, `Medium`, `High`).
11. **Real-World Sensor Noise**: ADC quantization noise, clock drift, and network packet jitter.
12. **Missing Data Injection**: Realistic 1.5% `NaN` values across communication and hardware sensors.
13. **Digital Twin Grid Operational Modes**: Dynamic global grid states (`Normal`, `Peak_Demand`, `Grid_Fault`, `Maintenance`, `Emergency`).
14. **Zero-Day Attack Isolation**: Classes 8 (*Firmware Attack*), 11 (*Insider Attack*), and 12 (*Malware*) are strictly isolated inside `zero_day_test.csv`.
15. **Multitask Label Hierarchy**: `is_attack`, `attack_domain`, `attack_type`, `attack_category`, `attack_severity`, `attack_stage`.
16. **Dataset Provenance & Versioning**: Embedded version string, timestamp, config hash, and seed control.
17. **Integrated ML & DL Baselines (`run_baselines.py`)**: Automated benchmarking for Logistic Regression, Random Forest, Extra Trees, MLP, and Zero-Day anomaly detection.
18. **Automated Publication Figures (`generate_figures.py`)**: Produces high-DPI Correlation Heatmaps, KDE Distributions, 2D PCA Projections, Confusion Matrices, and Feature Importance charts.
19. **Configurable Grid Scales**: Preset profiles (`small_grid`, `medium_grid`, `large_grid`, `city_grid`).

---

## 📊 Dataset Schema (54 Columns across 7 Domains)

| Domain | Feature Name | Data Type | Description |
| :--- | :--- | :--- | :--- |
| **Metadata** | `timestamp` | String ISO | 15-min sampling timestamp |
| | `meter_id`, `substation_id`, `feeder_id` | String | Grid hierarchy IDs |
| | `transformer_id`, `nan_id`, `dc_id` | String | Transformer, NAN, and Data Concentrator IDs |
| | `validator_group`, `location` | String | Blockchain validator group & spatial zone |
| | `consumer_type`, `grid_state`, `consensus_protocol` | String | Sector profile, Grid mode, BFT protocol |
| **Weather** | `ambient_temperature`, `humidity` | Float | Ambient temp (°C) & RH (%) |
| | `solar_irradiance`, `wind_speed` | Float | W/m² and m/s |
| | `time_of_day`, `day_of_week`, `is_holiday` | Float / Int | Diurnal hours, day index, holiday flag |
| **Electrical** | `voltage`, `current`, `frequency` | Float | Volts (229±2V), Amps, Hz (50±0.05Hz) |
| | `active_power`, `reactive_power`, `apparent_power` | Float | kW ($P=VI\cos\phi/1000$), kVAR, kVA |
| | `power_factor`, `energy`, `peak_demand`, `load_variance` | Float | $\cos\phi$, cumulative kWh, peak kW, variance |
| **Communication** | `packet_rate`, `packet_size`, `packet_delay` | Float | pps, Bytes, ms |
| | `packet_loss`, `retransmissions`, `rssi` | Float | %, count, dBm |
| | `encryption_enabled`, `authentication_success`, `signature_valid` | Float | Binary flags (1/0) |
| | `session_duration` | Float | Active session length (s) |
| **Device** | `cpu_usage`, `ram_usage`, `flash_usage` | Float | Hardware utilization % |
| | `temperature`, `battery`, `reboot_count` | Float | Operating temp (°C), health %, reboot count |
| | `firmware_hash_valid`, `secure_boot`, `tpm_status` | Float | Binary security state flags |
| **Blockchain** | `consensus_latency`, `transaction_delay` | Float | BFT consensus time (ms) & mempool delay |
| | `validator_votes`, `failed_consensus`, `block_interval` | Float | Vote count, failed rounds, block interval (s) |
| | `leader_change`, `queue_length`, `smart_contract_latency`, `byzantine_votes` | Float | View changes, tx queue, smart contract ms, malicious votes |
| **IDS Security** | `anomaly_score`, `entropy`, `packet_diversity` | Float | Statistical anomaly score, Shannon entropy, protocol diversity |
| | `drift_score`, `isolation_forest_score`, `autoencoder_score`, `svm_score` | Float | Concept drift, IF score, AE reconstruction loss, OC-SVM score |
| **Target Labels** | `attack_type`, `attack_category`, `attack_domain` | Int / String | Class ID (0-12), Category Name, Domain (Physical/Network/Device/Consensus) |
| | `attack_severity`, `attack_stage`, `affected_features`, `is_attack` | String / Int | Severity, Stage, XAI affected features list, Binary indicator |

---

## ⚡ Attack Taxonomy (13 Classes)

```
0: Normal                   - Standard grid operation
1: DoS                      - Network packet flooding & CPU depletion
2: DDoS                     - Distributed multi-source packet flooding
3: Replay                   - Re-transmission of valid signed telemetry with timestamp lag
4: MITM                     - Signature corruption & authentication interception
5: False Data Injection     - Physical voltage/power manipulation breaking P = VIcos(phi)
6: Sybil                    - Validator vote spoofing & identity flooding
7: Byzantine                - Consensus round disruption & contradictory voting
8: Firmware Attack          - [ZERO-DAY] Hash tampering, secure boot compromise, forced reboots
9: Key Theft                - Stolen cryptographic keys & unauthorized transaction signing
10: Data Tampering          - Energy counter corruption & oversized packet injection
11: Insider Attack          - [ZERO-DAY] Stealthy, low-rate physical energy under-reporting
12: Malware                 - [ZERO-DAY] CPU/RAM depletion, thermal elevation, flash wear
```

---

## 🚀 Quickstart & Usage

### 1. Installation
```bash
git clone https://github.com/your-username/ami-cpsd.git
cd ami-cpsd
pip install -r requirements.txt
```

### 2. Generate Dataset Splits
Generate the full **1,100,000 row** IEEE publication dataset:
```bash
python generate_dataset.py --profile large_grid
```
*For fast local testing, use `--profile small_grid` (11,000 rows) or `--profile medium_grid` (55,000 rows).*

This generates:
- `datasets/train.csv` (700,000 rows)
- `datasets/validation.csv` (150,000 rows)
- `datasets/test.csv` (150,000 rows)
- `datasets/zero_day_test.csv` (100,000 rows)
- `metadata/metadata.json` & `metadata/topology_graph.json`

### 3. Run Baseline ML & DL Benchmarks
Train Random Forest, Extra Trees, MLP, and evaluate Zero-Day detection:
```bash
python run_baselines.py
```

### 4. Auto-Generate Publication Paper Figures
Create high-DPI figures in `results/`:
```bash
python generate_figures.py
```

### 5. Verify Dataset Statistics
```bash
python summarize_dataset.py
```

---

## 📜 Citation

If you use **AMI-CPSD v1.0** in your research, please cite:

```bibtex
@article{ami_cpsd_2026,
  title={AI-Assisted Blockchain-Based Intrusion Detection for Advanced Metering Infrastructure (AMI)},
  journal={IEEE Transactions on Smart Grid},
  year={2026},
  publisher={IEEE}
}
```
