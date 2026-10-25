"""
Central Configuration for AMI-CPSD v2.0 Benchmark Suite.
Defines all features, labels, exclusions, and directories to prevent label leakage.
"""

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATASETS_DIR = BASE_DIR / "datasets"
RESULTS_DIR = BASE_DIR / "results"
REPORTS_DIR = RESULTS_DIR / "reports"
FIGURES_DIR = RESULTS_DIR / "figures"

# Ensure dirs exist
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Random seed
SEED = 42

# Label Columns & Metadata (MUST BE EXCLUDED FROM FEATURES)
LABEL_COL = "attack_type"
BINARY_LABEL_COL = "is_attack"

EXCLUDED_COLS = [
    "timestamp", "meter_id", "substation_id", "feeder_id", "transformer_id",
    "nan_id", "dc_id", "validator_group", "location", "consumer_type",
    "grid_state", "consensus_protocol",
    # Label and stage columns
    "attack_type", "attack_category", "attack_domain", "attack_severity",
    "attack_stage", "affected_features", "is_attack",
    "attack_start", "attack_end", "duration_sec", "recovery_time_sec",
]

# 52 Numeric Feature Columns
FEATURE_COLS = [
    "ambient_temperature", "humidity", "solar_irradiance", "wind_speed",
    "time_of_day", "day_of_week", "is_holiday",
    "voltage", "current", "frequency", "active_power", "reactive_power",
    "apparent_power", "power_factor", "energy", "peak_demand", "load_variance",
    "packet_rate", "packet_size", "packet_delay", "packet_loss", "retransmissions",
    "rssi", "encryption_enabled", "authentication_success", "signature_valid",
    "session_duration", "cpu_usage", "ram_usage", "flash_usage", "temperature",
    "battery", "firmware_hash_valid", "reboot_count", "secure_boot", "tpm_status",
    "consensus_latency", "transaction_delay", "validator_votes", "failed_consensus",
    "block_interval", "leader_change", "queue_length", "smart_contract_latency",
    "byzantine_votes", "anomaly_score", "entropy", "packet_diversity", "drift_score",
    "isolation_forest_score", "autoencoder_score", "svm_score"
]

# Attack mappings
ATTACK_NAMES = {
    0: "Normal",
    1: "False Data Injection",
    2: "Key Theft",
    3: "Replay",
    4: "MITM",
    5: "Sybil",
    6: "DoS",
    7: "Byzantine",
    8: "DDoS",
    9: "Data Tampering",
    10: "Insider Attack",
    11: "Malware",
    12: "Firmware Attack"
}
