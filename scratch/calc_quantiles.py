import json
import numpy as np
import os
import sys

sys.path.insert(0, r"c:\Users\athar\OneDrive\Desktop\vjti-comparison-bft-towerbft")
from probabilistic_model import latency_distribution, N_NODES

with open(r"c:\Users\athar\OneDrive\Desktop\vjti-comparison-bft-towerbft\protocols.json") as f:
    protocols = json.load(f)

np.random.seed(42)
n_samples = 100000
tau_samples = np.random.normal(50.0, 10.0, n_samples)
tau_samples = np.clip(tau_samples, 5.0, None)

print("--- LATENCY PERCENTILES (ms) ---")
for name, data in protocols.items():
    lat_nominal = data["latency_ms"]
    # Jitter simulation proportional to nominal or specific model
    if name == "OM(m)":
        arr = (16 + 1) * 51 * tau_samples
    elif name == "Classic PBFT":
        arr = 3 * 51 * tau_samples
    elif name == "Tower BFT":
        # Base latency = 2 * tau, f=16 attack + vc
        l_base = 2.0 * tau_samples
        l_attack = 16 * 2.5
        l_vc = (16 / 51) * 50.0
        arr = l_base + l_attack + l_vc + (242.9 - (2.0*50 + 16*2.5 + (16/51)*50.0))
    else:
        # Scale jitter proportional to nominal latency
        arr = lat_nominal * (tau_samples / 50.0)
    
    mean_val = np.mean(arr)
    med_val = np.median(arr)
    p95_val = np.percentile(arr, 95)
    p99_val = np.percentile(arr, 99)
    print(f"{name:15} | Nominal: {lat_nominal:7.1f} | Mean: {mean_val:8.2f} | Med: {med_val:8.2f} | P95: {p95_val:8.2f} | P99: {p99_val:8.2f}")
