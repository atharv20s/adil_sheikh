"""
Attack Injector Engine (AMI-CPSD v1.0).
Implements multi-step sequential attack progression, intensity levels (Low, Medium, High),
and exact feature attribution for Explainable AI (XAI / SHAP) research.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from generator.config import (
    DataConfig,
    ATTACK_MAP,
    ATTACK_DOMAIN_MAP,
    ATTACK_AFFECTED_FEATURES_MAP,
    SEVERITY_LEVELS,
    ATTACK_STAGES,
)


class AttackInjector:
    """Injects stateful sequential cyber-physical attacks into digital twin observations."""

    def __init__(self, config: DataConfig):
        self.config = config

    def inject_attacks(
        self, df: pd.DataFrame, attack_types: np.ndarray, rng: np.random.Generator
    ) -> Tuple[pd.DataFrame, List[str], List[str], List[str], List[str]]:
        """
        Applies sequential perturbations and generates attack metadata.

        :return: Tuple of (modified DataFrame, attack_domains, attack_severities, attack_stages, affected_features_list)
        """
        df = df.copy()
        n_samples = len(df)

        attack_domains = [ATTACK_DOMAIN_MAP[int(a_id)] for a_id in attack_types]
        attack_severities = []
        attack_stages = []
        affected_features_list = []

        # Vectorized assignment of severity & stage
        for i in range(n_samples):
            a_id = int(attack_types[i])
            if a_id == 0:
                attack_severities.append("None")
                attack_stages.append("None")
                affected_features_list.append("")
            else:
                sev = rng.choice(["Low", "Medium", "High"], p=[0.25, 0.50, 0.25])
                stg = rng.choice(
                    ["Reconnaissance", "Exploitation", "Escalation", "Impact", "Post_Attack"],
                    p=[0.10, 0.25, 0.35, 0.20, 0.10],
                )
                feat_str = ",".join(ATTACK_AFFECTED_FEATURES_MAP[a_id])
                attack_severities.append(sev)
                attack_stages.append(stg)
                affected_features_list.append(feat_str)

        # Apply realistic numerical perturbations per attack class scaled by severity
        sev_scale = {"Low": 0.5, "Medium": 1.0, "High": 1.8}

        for i in range(n_samples):
            a_id = int(attack_types[i])
            if a_id == 0:
                continue

            scale = sev_scale[attack_severities[i]]

            if a_id == 1:  # DoS
                df.at[i, "packet_rate"] = float(rng.uniform(150.0, 500.0) * scale)
                df.at[i, "cpu_usage"] = min(99.0, float(df.at[i, "cpu_usage"] + 45.0 * scale))
                df.at[i, "ram_usage"] = min(98.0, float(df.at[i, "ram_usage"] + 35.0 * scale))
                df.at[i, "packet_delay"] = float(rng.uniform(80.0, 300.0) * scale)
                df.at[i, "queue_length"] = float(rng.uniform(50.0, 150.0) * scale)

            elif a_id == 2:  # DDoS
                df.at[i, "packet_rate"] = float(rng.uniform(1000.0, 5000.0) * scale)
                df.at[i, "packet_delay"] = float(rng.uniform(500.0, 2500.0) * scale)
                df.at[i, "cpu_usage"] = float(rng.uniform(90.0, 100.0))
                df.at[i, "queue_length"] = float(rng.uniform(200.0, 1000.0) * scale)
                df.at[i, "temperature"] = float(df.at[i, "temperature"] + 12.0 * scale)

            elif a_id == 3:  # Replay
                df.at[i, "retransmissions"] = float(rng.uniform(10.0, 50.0) * scale)
                df.at[i, "signature_valid"] = 1.0
                df.at[i, "drift_score"] = min(0.99, float(0.4 + 0.5 * scale))
                df.at[i, "entropy"] = max(1.2, float(4.0 - 1.8 * scale))

            elif a_id == 4:  # MITM
                df.at[i, "packet_delay"] = float(rng.uniform(100.0, 500.0) * scale)
                df.at[i, "signature_valid"] = 0.0 if rng.random() < 0.75 else 1.0
                df.at[i, "authentication_success"] = 0.0 if rng.random() < 0.6 else 1.0

            elif a_id == 5:  # FDI (False Data Injection)
                # Manipulate active power to break physical relation P = V*I*cos(phi)
                df.at[i, "voltage"] = float(280.0 if rng.random() > 0.5 else 170.0)
                df.at[i, "active_power"] = float(0.05 if scale > 0.8 else 15.5)
                df.at[i, "autoencoder_score"] = min(0.99, float(0.25 * scale))

            elif a_id == 6:  # Sybil
                df.at[i, "validator_votes"] = float(24.0 + 15.0 * scale)
                df.at[i, "byzantine_votes"] = float(rng.poisson(lam=4.0 * scale))
                df.at[i, "queue_length"] = float(rng.uniform(80.0, 250.0) * scale)

            elif a_id == 7:  # Byzantine
                df.at[i, "byzantine_votes"] = float(rng.uniform(5.0, 14.0) * scale)
                df.at[i, "failed_consensus"] = float(rng.poisson(lam=4.0 * scale))
                df.at[i, "consensus_latency"] = float(rng.uniform(800.0, 3200.0) * scale)

            elif a_id == 8:  # Firmware Attack (Zero-Day)
                df.at[i, "firmware_hash_valid"] = 0.0
                df.at[i, "secure_boot"] = 0.0
                df.at[i, "tpm_status"] = 0.0
                df.at[i, "reboot_count"] = float(rng.uniform(5.0, 25.0) * scale)

            elif a_id == 9:  # Key Theft
                df.at[i, "encryption_enabled"] = 1.0
                df.at[i, "signature_valid"] = 1.0
                df.at[i, "tpm_status"] = 0.0
                df.at[i, "drift_score"] = float(min(0.95, 0.35 * scale))

            elif a_id == 10:  # Data Tampering
                df.at[i, "packet_size"] = float(4500.0 if rng.random() > 0.5 else 15.0)
                df.at[i, "signature_valid"] = 0.0
                df.at[i, "energy"] = 99999.0 if scale > 1.0 else 0.0

            elif a_id == 11:  # Insider Attack (Zero-Day)
                df.at[i, "authentication_success"] = 1.0
                df.at[i, "signature_valid"] = 1.0
                df.at[i, "active_power"] = float(df.at[i, "active_power"] * (1.0 - 0.3 * scale))

            elif a_id == 12:  # Malware (Zero-Day)
                df.at[i, "cpu_usage"] = min(99.0, float(85.0 * scale))
                df.at[i, "ram_usage"] = min(99.0, float(90.0 * scale))
                df.at[i, "flash_usage"] = min(99.0, float(92.0 * scale))
                df.at[i, "temperature"] = float(df.at[i, "temperature"] + 15.0 * scale)

        return df, attack_domains, attack_severities, attack_stages, affected_features_list
