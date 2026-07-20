import os
import shutil
from html2image import Html2Image

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
hti = Html2Image(browser_executable=edge_path, output_path="figures")

os.makedirs("figures", exist_ok=True)

# ---------------------------------------------------------
# 1. Figure 8 & 13: Comparative Security Causal Workflow
# ---------------------------------------------------------
html_workflow = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: #ffffff;
  margin: 0;
  padding: 40px;
  width: 1100px;
  box-sizing: border-box;
  color: #0f172a;
}

.title-container {
  text-align: center;
  margin-bottom: 30px;
}

.title {
  font-size: 24px;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.5px;
}

.subtitle {
  font-size: 14px;
  color: #64748b;
  margin-top: 6px;
  font-weight: 500;
}

.workflow-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 950px;
  margin: 0 auto;
}

.step-card {
  display: flex;
  align-items: center;
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 14px;
  padding: 18px 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  transition: all 0.2s ease;
}

.step-number {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 18px;
  margin-right: 20px;
  flex-shrink: 0;
}

.step-1 .step-number { background: #fee2e2; color: #991b1b; }
.step-2 .step-number { background: #ffedd5; color: #c2410c; }
.step-3 .step-number { background: #fef3c7; color: #b45309; }
.step-4 .step-number { background: #dcfce7; color: #15803d; }
.step-5 .step-number { background: #e0f2fe; color: #0369a1; }
.step-6 .step-number { background: #f0fdf4; color: #166534; border: 2px solid #22c55e; }

.step-content {
  flex-grow: 1;
}

.step-title {
  font-size: 16px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 4px 0;
}

.step-desc {
  font-size: 13.5px;
  color: #475569;
  margin: 0;
  line-height: 1.4;
}

.arrow-divider {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 12px;
  color: #94a3b8;
}

.arrow-divider svg {
  width: 20px;
  height: 20px;
  fill: #94a3b8;
}

.metric-pill {
  background: #166534;
  color: white;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12.5px;
  font-weight: 700;
  margin-left: 16px;
  flex-shrink: 0;
}
</style>
</head>
<body>
<div class="title-container">
  <div class="title">Comparative Application Security Workflow</div>
  <div class="subtitle">Causal Validation Pipeline: Converting Attack Ingress to Quantified Security Gains under STSF</div>
</div>

<div class="workflow-grid">
  <div class="step-card step-1">
    <div class="step-number">1</div>
    <div class="step-content">
      <div class="step-title">Cyber-Physical Attack Vector Ingress</div>
      <div class="step-desc">False Data Injection (FDI), MitM, Replay, DoS/DDoS, Sybil, and Byzantine Node Infiltration</div>
    </div>
  </div>

  <div class="arrow-divider"><svg viewBox="0 0 24 24"><path d="M12 16l-6-6h12z"/></svg></div>

  <div class="step-card step-2">
    <div class="step-number">2</div>
    <div class="step-content">
      <div class="step-title">Proactive Cryptographic Hash Verification</div>
      <div class="step-desc">SHA-256 Payload Integrity Check & Nonce Timestamping (Neutralizes Replay Vectors)</div>
    </div>
  </div>

  <div class="arrow-divider"><svg viewBox="0 0 24 24"><path d="M12 16l-6-6h12z"/></svg></div>

  <div class="step-card step-3">
    <div class="step-number">3</div>
    <div class="step-content">
      <div class="step-title">Distributed BFT Consensus Engine</div>
      <div class="step-desc">Multi-Validator Binomial Voting Quorums ($n=51, f=16$, $P_{\text{SPOF}} \to 10^{-10}$)</div>
    </div>
  </div>

  <div class="arrow-divider"><svg viewBox="0 0 24 24"><path d="M12 16l-6-6h12z"/></svg></div>

  <div class="step-card step-4">
    <div class="step-number">4</div>
    <div class="step-content">
      <div class="step-title">Multi-Signature Quorum Validation</div>
      <div class="step-desc">Threshold Signature Verification & Shamir Secret Key Share Recovery</div>
    </div>
  </div>

  <div class="arrow-divider"><svg viewBox="0 0 24 24"><path d="M12 16l-6-6h12z"/></svg></div>

  <div class="step-card step-5">
    <div class="step-number">5</div>
    <div class="step-content">
      <div class="step-title">Sub-Second Exposure Window Reduction</div>
      <div class="step-desc">Pipelined Finality ($L=200\text{ms}$), suppressing Poisson Exposure Window ($W(\tau) < 0.024$)</div>
    </div>
  </div>

  <div class="arrow-divider"><svg viewBox="0 0 24 24"><path d="M12 16l-6-6h12z"/></svg></div>

  <div class="step-card step-6">
    <div class="step-number">6</div>
    <div class="step-content">
      <div class="step-title">Quantified Security Improvement (STSF Framework)</div>
      <div class="step-desc">Static BFT Gain ($10^{170}$ Orders), Realized Security ($P_{\text{secure}} \ge 0.927$), Coordinator SPOF Eliminated</div>
    </div>
    <div class="metric-pill">+170 Orders Gain</div>
  </div>
</div>
</body>
</html>
"""

with open("figures/fig13_workflow.html", "w", encoding="utf-8") as f:
    f.write(html_workflow)

hti.screenshot(html_file="figures/fig13_workflow.html", save_as="fig_comparative_workflow.png", size=(1100, 780))
shutil.copy("figures/fig_comparative_workflow.png", "fig_comparative_workflow.png")


# ---------------------------------------------------------
# 2. Figure 10: Model Comparison (Sheikh vs Parallel)
# ---------------------------------------------------------
html_model_comp = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

body {
  font-family: 'Inter', system-ui, sans-serif;
  background: #ffffff;
  margin: 0;
  padding: 40px;
  width: 1100px;
  box-sizing: border-box;
  color: #0f172a;
}

.title-container {
  text-align: center;
  margin-bottom: 30px;
}

.title {
  font-size: 24px;
  font-weight: 800;
  color: #0f172a;
}

.subtitle {
  font-size: 14px;
  color: #64748b;
  margin-top: 6px;
}

.comp-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  max-width: 1000px;
  margin: 0 auto;
}

.comp-card {
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
}

.card-header {
  font-size: 16px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tag {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 12px;
}

.tag-blue { background: #e0f2fe; color: #0369a1; }
.tag-purple { background: #f3e8ff; color: #6b21a8; }

.metric-row {
  margin-bottom: 20px;
}

.metric-label {
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  margin-bottom: 6px;
  display: flex;
  justify-content: space-between;
}

.bar-bg {
  background: #e2e8f0;
  height: 14px;
  border-radius: 7px;
  overflow: hidden;
}

.bar-fill-red { background: linear-gradient(90deg, #ef4444, #dc2626); height: 100%; border-radius: 7px; }
.bar-fill-green { background: linear-gradient(90deg, #22c55e, #16a34a); height: 100%; border-radius: 7px; }

.val-box {
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  padding: 12px;
  font-size: 13px;
  color: #334155;
  margin-top: 14px;
  line-height: 1.4;
}
</style>
</head>
<body>
<div class="title-container">
  <div class="title">Security Model Comparison: Single-Target vs. Parallel Failure</div>
  <div class="subtitle">Contrasting Sheikh et al.'s Target Attack Model ($P_{\text{TA}}$) against Parallel System Compromise ($P_{\text{Compromise}}$)</div>
</div>

<div class="comp-grid">
  <!-- Card 1 -->
  <div class="comp-card">
    <div class="card-header">
      <span>Sheikh Target Attack Model</span>
      <span class="tag tag-blue">Single Target ($P_{\text{TA}}$)</span>
    </div>
    
    <div class="metric-row">
      <div class="metric-label"><span>Without Blockchain (Baseline)</span><b>P = 0.0050 (0.5%)</b></div>
      <div class="bar-bg"><div class="bar-fill-red" style="width: 5%;"></div></div>
    </div>

    <div class="metric-row">
      <div class="metric-label"><span>With BFT Blockchain</span><b>P = 10⁻¹⁷³ (Static)</b></div>
      <div class="bar-bg"><div class="bar-fill-green" style="width: 0.1%;"></div></div>
    </div>

    <div class="val-box">
      <b>Assumes:</b> Arithmetic mean across 4 subsystem targets under uniform probability ($1/4$). Valid for single-target expected value calculation.
    </div>
  </div>

  <!-- Card 2 -->
  <div class="comp-card">
    <div class="card-header">
      <span>Parallel System Compromise</span>
      <span class="tag tag-purple">Worst-Case ($P_{\text{Compromise}}$)</span>
    </div>
    
    <div class="metric-row">
      <div class="metric-label"><span>Without Blockchain (Baseline)</span><b>P = 0.9740 (97.4%)</b></div>
      <div class="bar-bg"><div class="bar-fill-red" style="width: 97.4%;"></div></div>
    </div>

    <div class="metric-row">
      <div class="metric-label"><span>With BFT Blockchain</span><b>P = 5.99 × 10⁻⁷</b></div>
      <div class="bar-bg"><div class="bar-fill-green" style="width: 0.1%;"></div></div>
    </div>

    <div class="val-box">
      <b>Assumes:</b> Parallel exposure across 12 cyber-physical attack vectors. Reveals that centralized systems are <b>97.4% compromised</b> without BFT consensus.
    </div>
  </div>
</div>
</body>
</html>
"""

with open("figures/fig10_model_comparison.html", "w", encoding="utf-8") as f:
    f.write(html_model_comp)

hti.screenshot(html_file="figures/fig10_model_comparison.html", save_as="fig_model_comparison.png", size=(1100, 580))
shutil.copy("figures/fig_model_comparison.png", "fig_model_comparison.png")

print("All HTML/CSS publication-quality rendered figures successfully generated!")
