"""
Generates the Visual Attack Timeline Figure for AMI-CPSD v3.0.
Plots the causal progression: Normal -> Recon -> Exploit -> Consensus Delay -> Packet Loss -> IDS Alert -> Recovery.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

RESULTS_DIR = Path("results/figures")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def generate_attack_timeline():
    fig, axes = plt.subplots(4, 1, figsize=(12, 8), sharex=True)
    time_steps = np.arange(0, 100)

    # 1. Attack Lifecycle Stage & CPU Usage
    cpu_usage = np.full(100, 15.0)
    cpu_usage[20:30] = np.linspace(15, 35, 10)  # Recon
    cpu_usage[30:50] = np.linspace(35, 85, 20)  # Exploit / Injection
    cpu_usage[50:75] = 95.0                     # Impact
    cpu_usage[75:100] = np.linspace(95, 15, 25) # Recovery

    axes[0].plot(time_steps, cpu_usage, color="crimson", lw=2, label="Smart Meter CPU Usage (%)")
    axes[0].axvspan(20, 30, color="gold", alpha=0.3, label="Reconnaissance")
    axes[0].axvspan(30, 50, color="orange", alpha=0.3, label="Exploitation")
    axes[0].axvspan(50, 75, color="red", alpha=0.3, label="Impact (FDI Attack)")
    axes[0].axvspan(75, 100, color="green", alpha=0.2, label="Recovery")
    axes[0].set_ylabel("CPU Usage (%)")
    axes[0].legend(loc="upper left", fontsize=9)
    axes[0].set_title("AMI-CPSD v3.0 Causal Cyber-Physical Attack Lifecycle Timeline", fontsize=13, fontweight="bold")
    axes[0].grid(True, linestyle="--", alpha=0.5)

    # 2. Voltage & Active Power (Physics)
    voltage = 230.0 + np.random.normal(0, 0.5, 100)
    voltage[50:75] = 275.0 # FDI attack voltage manipulation
    active_power = (voltage * 10.0 * 0.92) / 1000.0
    active_power[50:75] = 0.05 # Manipulated power

    axes[1].plot(time_steps, voltage, color="darkblue", lw=2, label="Voltage (V)")
    axes[1].axhline(250.0, color="red", linestyle=":", label="Overvoltage Threshold (250V)")
    axes[1].set_ylabel("Voltage (V)")
    axes[1].legend(loc="upper left", fontsize=9)
    axes[1].grid(True, linestyle="--", alpha=0.5)

    # 3. Consensus Latency & Queue Backlog (Closed-Loop Feedback)
    consensus_lat = np.full(100, 120.0)
    consensus_lat[40:75] = np.linspace(120, 1450, 35) # Byzantine retries
    consensus_lat[75:100] = np.linspace(1450, 120, 25)

    axes[2].plot(time_steps, consensus_lat, color="purple", lw=2, label="PBFT Consensus Latency (ms)")
    axes[2].set_ylabel("Latency (ms)")
    axes[2].legend(loc="upper left", fontsize=9)
    axes[2].grid(True, linestyle="--", alpha=0.5)

    # 4. IDS Anomaly Alert Score
    ids_score = np.full(100, 0.05)
    ids_score[30:50] = np.linspace(0.05, 0.45, 20)
    ids_score[50:75] = 0.95 # Alert triggered!
    ids_score[75:100] = np.linspace(0.95, 0.05, 25)

    axes[3].plot(time_steps, ids_score, color="darkgreen", lw=2, label="PINN / Multi-Task IDS Anomaly Score")
    axes[3].axhline(0.50, color="red", linestyle="--", label="Alert Threshold (0.50)")
    axes[3].set_xlabel("Simulation Ticks (15-min intervals)")
    axes[3].set_ylabel("IDS Score")
    axes[3].legend(loc="upper left", fontsize=9)
    axes[3].grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    out_path = RESULTS_DIR / "attack_timeline.png"
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Saved attack timeline visualization to {out_path}")

if __name__ == "__main__":
    generate_attack_timeline()
