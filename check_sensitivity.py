from probabilistic_model import sensitivity_ranking

r = sensitivity_ranking(latency_ms=242.9, lambda_attack=20.0)
print("Tower BFT lambda=20:")
for k, v in r.items():
    print(f"  {k}: {v:.2f}%")
total_temp = r["Latency (L)"] + r["Attack rate (lambda)"]
total_stat = r["Receiver (P_R)"] + r["SCADA (P_SCADA)"]
print(f"  Total Temporal: {total_temp:.2f}%")
print(f"  Total Static: {total_stat:.2f}%")

print()
r2 = sensitivity_ranking(latency_ms=7650.0, lambda_attack=1.0)
print("Classic PBFT lambda=1:")
for k, v in r2.items():
    print(f"  {k}: {v:.2f}%")
total_temp2 = r2["Latency (L)"] + r2["Attack rate (lambda)"]
total_stat2 = r2["Receiver (P_R)"] + r2["SCADA (P_SCADA)"]
print(f"  Total Temporal: {total_temp2:.2f}%")
print(f"  Total Static: {total_stat2:.2f}%")
