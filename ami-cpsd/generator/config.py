"""
Config module for AMI Cyber-Physical Digital Twin Dataset (AMI-CPSD v1.0).
Defines grid profiles, BFT consensus protocols, attack taxonomies, severity levels,
feature domain categories, and simulation parameters.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

# Versioning and Provenance
DATASET_VERSION = "AMI-CPSD v1.0"
GENERATOR_VERSION = "1.0.0"

# Attack Taxonomy (13 Classes)
ATTACK_MAP: Dict[int, str] = {
    0: "Normal",
    1: "DoS",
    2: "DDoS",
    3: "Replay",
    4: "MITM",
    5: "False Data Injection",
    6: "Sybil",
    7: "Byzantine",
    8: "Firmware Attack",
    9: "Key Theft",
    10: "Data Tampering",
    11: "Insider Attack",
    12: "Malware",
}

# High-Level Attack Domains for Multi-Task Learning
ATTACK_DOMAIN_MAP: Dict[int, str] = {
    0: "Normal",
    1: "Network",
    2: "Network",
    3: "Network",
    4: "Network",
    5: "Physical",
    6: "Consensus",
    7: "Consensus",
    8: "Device",
    9: "Consensus",
    10: "Physical",
    11: "Physical",
    12: "Device",
}

# Attack Affected Features Ground-Truth (For XAI / SHAP Evaluation)
ATTACK_AFFECTED_FEATURES_MAP: Dict[int, List[str]] = {
    0: [],
    1: ["packet_rate", "cpu_usage", "ram_usage", "packet_delay", "packet_loss", "queue_length"],
    2: ["packet_rate", "packet_delay", "packet_loss", "cpu_usage", "ram_usage", "queue_length", "temperature"],
    3: ["retransmissions", "drift_score", "packet_diversity", "entropy", "isolation_forest_score"],
    4: ["packet_delay", "signature_valid", "authentication_success", "packet_diversity", "svm_score"],
    5: ["voltage", "current", "active_power", "energy", "autoencoder_score", "isolation_forest_score"],
    6: ["validator_votes", "leader_change", "entropy", "byzantine_votes", "queue_length"],
    7: ["byzantine_votes", "failed_consensus", "leader_change", "consensus_latency", "smart_contract_latency"],
    8: ["firmware_hash_valid", "secure_boot", "reboot_count", "cpu_usage", "temperature", "tpm_status"],
    9: ["tpm_status", "session_duration", "byzantine_votes", "drift_score"],
    10: ["packet_size", "signature_valid", "drift_score", "energy"],
    11: ["active_power", "drift_score", "anomaly_score"],
    12: ["cpu_usage", "ram_usage", "flash_usage", "temperature", "reboot_count", "entropy"],
}

# Zero-Day attack classes (excluded from Train, Validation, and Test; present ONLY in zero_day_test.csv)
ZERO_DAY_ATTACKS: List[int] = [8, 11, 12]  # Firmware Attack, Insider Attack, Malware

# Standard attacks (used in Train, Validation, and Test datasets)
STANDARD_ATTACKS: List[int] = [0, 1, 2, 3, 4, 5, 6, 7, 9, 10]

# Supported BFT Consensus Protocols
CONSENSUS_PROTOCOLS: List[str] = ["PBFT", "IBFT", "QBFT", "TowerBFT", "RVR_BFT"]

# Digital Twin Global Grid States
GRID_STATES: List[str] = ["Normal", "Peak_Demand", "Grid_Fault", "Maintenance", "Emergency"]

# Attack Severity Levels
SEVERITY_LEVELS: List[str] = ["None", "Low", "Medium", "High"]

# Attack Progression Stages (Sequential Multi-Step Attack Lifecycle)
ATTACK_STAGES: List[str] = ["None", "Reconnaissance", "Exploitation", "Escalation", "Impact", "Post_Attack"]

# Default Attack Probabilities for Train/Val/Test
STANDARD_ATTACK_DISTRIBUTION: Dict[int, float] = {
    0: 0.65, 1: 0.04, 2: 0.03, 3: 0.04, 4: 0.04, 5: 0.05, 6: 0.04, 7: 0.04, 9: 0.04, 10: 0.03,
}

# Attack distribution for Zero-Day test dataset
ZERO_DAY_ATTACK_DISTRIBUTION: Dict[int, float] = {
    0: 0.50, 1: 0.03, 2: 0.02, 3: 0.03, 4: 0.03, 5: 0.03, 6: 0.03, 7: 0.03, 8: 0.07, 9: 0.03, 10: 0.02, 11: 0.07, 12: 0.07,
}

# Feature Domain Categorization
METADATA_FEATURES: List[str] = [
    "timestamp",
    "meter_id",
    "substation_id",
    "feeder_id",
    "transformer_id",
    "nan_id",
    "dc_id",
    "validator_group",
    "location",
    "consumer_type",
    "grid_state",
    "consensus_protocol",
]

WEATHER_FEATURES: List[str] = [
    "ambient_temperature",
    "humidity",
    "solar_irradiance",
    "wind_speed",
    "time_of_day",
    "day_of_week",
    "is_holiday",
]

ELECTRICAL_FEATURES: List[str] = [
    "voltage",
    "current",
    "frequency",
    "active_power",
    "reactive_power",
    "apparent_power",
    "power_factor",
    "energy",
    "peak_demand",
    "load_variance",
]

COMMUNICATION_FEATURES: List[str] = [
    "packet_rate",
    "packet_size",
    "packet_delay",
    "packet_loss",
    "retransmissions",
    "rssi",
    "encryption_enabled",
    "authentication_success",
    "signature_valid",
    "session_duration",
]

DEVICE_FEATURES: List[str] = [
    "cpu_usage",
    "ram_usage",
    "flash_usage",
    "temperature",
    "battery",
    "firmware_hash_valid",
    "reboot_count",
    "secure_boot",
    "tpm_status",
]

BLOCKCHAIN_FEATURES: List[str] = [
    "consensus_latency",
    "transaction_delay",
    "validator_votes",
    "failed_consensus",
    "block_interval",
    "leader_change",
    "queue_length",
    "smart_contract_latency",
    "byzantine_votes",
]

IDS_FEATURES: List[str] = [
    "anomaly_score",
    "entropy",
    "packet_diversity",
    "drift_score",
    "isolation_forest_score",
    "autoencoder_score",
    "svm_score",
]

ALL_ENGINEERED_FEATURES: List[str] = (
    METADATA_FEATURES
    + WEATHER_FEATURES
    + ELECTRICAL_FEATURES
    + COMMUNICATION_FEATURES
    + DEVICE_FEATURES
    + BLOCKCHAIN_FEATURES
    + IDS_FEATURES
)

TARGET_LABEL_COLUMNS: List[str] = [
    "attack_type",
    "attack_category",
    "attack_domain",
    "attack_severity",
    "attack_stage",
    "affected_features",
    "is_attack",
]

ALL_FEATURES: List[str] = ALL_ENGINEERED_FEATURES + TARGET_LABEL_COLUMNS


@dataclass
class DataConfig:
    """Master Configuration parameters for dataset generation."""
    profile_name: str = "large_grid"
    num_substations: int = 2
    num_feeders: int = 6
    num_transformers: int = 20
    num_meters: int = 100
    num_nans: int = 10
    num_dcs: int = 4
    num_validator_groups: int = 8
    
    # Dataset Row Sizes (Default Large Grid)
    train_rows: int = 700000
    val_rows: int = 150000
    test_rows: int = 150000
    zero_day_rows: int = 100000
    
    # Random Seeds
    train_seed: int = 42
    val_seed: int = 43
    test_seed: int = 44
    zero_day_seed: int = 45
    
    # Missing Data Injection Percentage (1% - 3%)
    missing_data_pct: float = 0.015
    
    # Physics parameters
    nominal_voltage: float = 229.0
    voltage_std: float = 2.0
    nominal_frequency: float = 50.0
    frequency_std: float = 0.05
    physics_tolerance_kw: float = 0.05

    @classmethod
    def from_profile(cls, profile_name: str = "large_grid") -> "DataConfig":
        """Factory method to load configuration presets."""
        if profile_name == "small_grid":
            return cls(
                profile_name="small_grid",
                train_rows=7000,
                val_rows=1500,
                test_rows=1500,
                zero_day_rows=1000,
                num_meters=20,
            )
        elif profile_name == "medium_grid":
            return cls(
                profile_name="medium_grid",
                train_rows=35000,
                val_rows=7500,
                test_rows=7500,
                zero_day_rows=5000,
                num_meters=50,
            )
        elif profile_name == "large_grid":
            return cls(profile_name="large_grid")  # Default 1.1M rows
        elif profile_name == "city_grid":
            return cls(
                profile_name="city_grid",
                train_rows=3500000,
                val_rows=750000,
                test_rows=750000,
                zero_day_rows=500000,
                num_meters=500,
            )
        else:
            raise ValueError(f"Unknown grid profile: {profile_name}")
