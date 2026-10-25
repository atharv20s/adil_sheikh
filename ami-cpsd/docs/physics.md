# Smart Grid Cyber-Physical System Physics & Equations

This document details the core physical laws and continuous stochastic differential equations governing the **AMI-CPSD v2.0** Digital Twin.

---

## 1. Electrical Power Flow Equations

Smart meter observations adhere strictly to AC power flow laws:

### Active Power ($P$)
$$P = \frac{V \cdot I \cdot \cos\phi}{1000} \quad [\text{kW}]$$

where:
- $V$ = Voltage (Volts, nominal $229\text{ V} \pm 2\text{V}$)
- $I$ = Current (Amperes, $1.0\text{ A}$ – $50.0\text{ A}$)
- $\cos\phi$ = Power Factor ($0.80$ – $0.999$)

### Reactive Power ($Q$)
$$Q = P \cdot \tan(\arccos(\cos\phi)) \quad [\text{kVAR}]$$

### Apparent Power ($S$)
$$S = \sqrt{P^2 + Q^2} \quad [\text{kVA}]$$

### Cumulative Energy ($E$)
$$E(t) = \int_{0}^{t} P(\tau) \, d\tau \approx \sum_{k=1}^{N} P_k \cdot \Delta t \quad [\text{kWh}]$$

---

## 2. Temporal State Dynamics: Ornstein–Uhlenbeck SDE

To eliminate non-physical jump discontinuities between consecutive 15-minute sampling timestamps, state variables ($V, I, f, T_{\text{cpu}}$) evolve continuously via the mean-reverting **Ornstein–Uhlenbeck (OU)** Stochastic Differential Equation (SDE):

$$dx_t = \theta (\mu - x_t) \, dt + \sigma \, dW_t$$

Discrete Euler-Maruyama discretization:
$$x_{k+1} = x_k + \theta (\mu - x_k) \Delta t + \sigma \sqrt{\Delta t} \cdot \epsilon_k, \quad \epsilon_k \sim \mathcal{N}(0, 1)$$

Parameters:
- $\theta$: Mean-reversion rate coefficient
- $\mu$: Long-term equilibrium mean (e.g., $229\text{V}$ for voltage)
- $\sigma$: Volatility parameter
