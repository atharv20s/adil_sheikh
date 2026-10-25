# Walkthrough - AMI-CPSD v2.0 Modular Architecture & Streaming Generation

The **AMI Cyber-Physical Digital Twin (`AMI-CPSD v2.0`)** dataset generator has been refactored into a modular research simulator.

---

## 🌟 Key Architecture & Components

```
ami-cpsd/
├── simulator/             (Core physics, weather, topology, consumer profiles, scenario engine)
│   ├── scenario.py        (Scenario engine: Scenario(weather, profile, attack, grid_mode, protocol))
│   ├── physics.py         (OU process, P=VIcos(phi) validation, sensor noise)
│   ├── weather.py         (Diurnal environmental conditions)
│   ├── topology.py        (Substation -> Feeder -> Transformer -> Meter hierarchy)
│   └── profiles.py        (Residential, Commercial, Industrial load dynamics)
├── attacks/               (Object-Oriented Pluggable Attack Engine)
│   ├── base.py            (Base Attack class with apply(), severity(), affected_features(), stage())
│   ├── dos.py, ddos.py, replay.py, mitm.py, fdi.py, sybil.py, byzantine.py, firmware.py, key_theft.py, data_tampering.py, insider.py, malware.py
│   └── registry.py        (Attack factory registry)
├── blockchain/            (BFT consensus engines: PBFT, IBFT, QBFT, TowerBFT, RVR_BFT)
├── configs/               (YAML config files: small.yaml, medium.yaml, large.yaml, city.yaml)
├── benchmark/             (Model trainers: RF, ExtraTrees, Logistic Regression, MLP)
├── evaluation/            (Metrics, confusion matrices, SHAP evaluation - separate from generator!)
├── tests/                 (Unit tests: test_physics.py, test_weather.py, test_attacks.py, test_topology.py)
├── docs/                  (Paper equations & specs: physics.md, topology.md, attacks.md, features.md)
├── datasets/              (CSV & Parquet split files, nodes.csv, edges.csv, events.csv)
├── figures/               (High-DPI paper figures)
├── generate_dataset.py    (Master 100k-row chunked streaming generation script)
├── run_experiments.py     (Unified benchmark pipeline)
├── requirements.txt
└── README.md
```

---

## 🔬 Key Refactoring Highlights

1. **Streaming 100k-Row Chunked Dataset Generator (`generate_dataset.py`)**:
   - Streams CSV and Parquet output in `CHUNK_SIZE = 100_000` row batches (`mode="a"` append mode).
   - Low memory footprint (<300MB RAM).
   - Exact split targets:
     - `train.csv` (700,000 rows)
     - `validation.csv` (150,000 rows)
     - `test.csv` (150,000 rows)
     - `zero_day_test.csv` (100,000 rows)
     - **Total: 1,100,000 rows**.

2. **Object-Oriented Pluggable Attack Architecture (`attacks/`)**:
   - Base `Attack` class with methods `apply()`, `severity()`, `affected_features()`, `stage()`.
   - Pluggable attack classes for all 13 attack types.

3. **Scenario Engine (`simulator/scenario.py`)**:
   - Reusable scenarios: `Scenario(weather="summer", consumer_profile="residential", attack="DoS", grid_mode="Peak", protocol="PBFT")`.

4. **YAML Configuration System (`configs/`)**:
   - YAML files (`small.yaml`, `medium.yaml`, `large.yaml`, `city.yaml`).

5. **GNN Graph Node & Edge Exporter (`nodes.csv` & `edges.csv`)**:
   - Node list (`nodes.csv`) and edge list (`edges.csv`) for PyG, DGL, and NetworkX.

6. **Event Timeline Logging (`events.csv`)**:
   - Event timeline (`timestamp`, `meter_id`, `event_type`, `stage`, `details`) and timeline features (`attack_start`, `attack_end`, `duration`, `recovery_time`).

7. **Unit Test Suite (`tests/`)**:
   - PyTest test cases verifying physics bounds, weather equations, and pluggable attack registry (3/3 tests passing).

8. **Mathematical Documentation (`docs/`)**:
   - `physics.md`, `topology.md`, `attacks.md`, `features.md`.
