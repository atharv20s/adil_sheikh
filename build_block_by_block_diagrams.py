import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# IEEE Publication Typography
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'Liberation Serif']
plt.rcParams['font.size'] = 11

os.makedirs("figures", exist_ok=True)

# -------------------------------------------------------------------
# 1. Figure 13 / Fig 8 — Comparative Security Workflow (Block-by-Block)
# -------------------------------------------------------------------
def generate_block_workflow():
    fig, ax = plt.subplots(figsize=(9.5, 9.5), dpi=300)
    ax.axis('off')
    
    # 6 Blocks with clear step numbers, colors, titles, and descriptions
    blocks = [
        {
            "num": "1",
            "title": "Cyber-Physical Attack Vector Ingress",
            "desc": "False Data Injection (FDI), MitM, Replay, DoS/DDoS, Sybil & Byzantine Infiltration",
            "bg": "#fee2e2", "border": "#dc2626", "text_col": "#991b1b",
            "arrow_text": "Unverified Data & Raw Packet Ingress"
        },
        {
            "num": "2",
            "title": "Proactive Cryptographic Hash Verification",
            "desc": "SHA-256 Payload Integrity Check & Nonce Timestamping (Disables Replay Attacks)",
            "bg": "#ffedd5", "border": "#ea580c", "text_col": "#c2410c",
            "arrow_text": "Cryptographically Sealed Payloads"
        },
        {
            "num": "3",
            "title": "Distributed BFT Consensus Engine",
            "desc": "Multi-Validator Voting Quorums (n = 51, f = 16, SPOF Risk P_SPOF → 10⁻¹⁰)",
            "bg": "#fef3c7", "border": "#d97706", "text_col": "#b45309",
            "arrow_text": "Byzantine & Sybil Identities Rejected"
        },
        {
            "num": "4",
            "title": "Multi-Signature Quorum Validation",
            "desc": "Threshold Signature Verification & Shamir Secret Key Share Recovery",
            "bg": "#dcfce7", "border": "#16a34a", "text_col": "#15803d",
            "arrow_text": "Quorum Agreement Established"
        },
        {
            "num": "5",
            "title": "Sub-Second Exposure Window Reduction",
            "desc": "Pipelined Finality (L = 200 ms), Suppressing Poisson Exposure (W(τ) < 0.024)",
            "bg": "#e0f2fe", "border": "#0284c7", "text_col": "#0369a1",
            "arrow_text": "Minimized Exposure Window"
        },
        {
            "num": "6",
            "title": "Quantified Security Gain (STSF Framework)",
            "desc": "Static Gain: ~170 Orders | Realized Security: P_secure ≥ 0.927 | Coordinator SPOF Neutralized",
            "bg": "#f0fdf4", "border": "#15803d", "text_col": "#166534",
            "arrow_text": None
        }
    ]
    
    y_positions = [0.88, 0.72, 0.56, 0.40, 0.24, 0.08]
    box_height = 0.095
    box_width = 0.84
    box_x = 0.08
    
    for i, b in enumerate(blocks):
        y = y_positions[i]
        
        # Main Block Container
        rect = patches.FancyBboxPatch(
            (box_x, y - box_height/2), box_width, box_height,
            boxstyle="round,pad=0.01,rounding_size=0.02",
            fc=b["bg"], ec=b["border"], lw=1.8
        )
        ax.add_patch(rect)
        
        # Step Number Badge
        badge_size = 0.06
        badge = patches.FancyBboxPatch(
            (box_x + 0.02, y - badge_size/2), badge_size, badge_size,
            boxstyle="round,pad=0.005,rounding_size=0.01",
            fc=b["border"], ec=b["border"]
        )
        ax.add_patch(badge)
        ax.text(box_x + 0.05, y, b["num"], ha='center', va='center', color='white', fontweight='bold', fontsize=12)
        
        # Title and Description Text
        ax.text(box_x + 0.10, y + 0.02, b["title"], ha='left', va='center', fontweight='bold', fontsize=11.5, color='#0f172a')
        ax.text(box_x + 0.10, y - 0.02, b["desc"], ha='left', va='center', fontsize=9.5, color='#334155')
        
        # Arrow and Arrow Label (No Overlap!)
        if b["arrow_text"] is not None:
            next_y = y_positions[i+1]
            arrow_start_y = y - box_height/2 - 0.005
            arrow_end_y = next_y + box_height/2 + 0.005
            mid_y = (arrow_start_y + arrow_end_y) / 2.0
            
            # Vertical Arrow
            ax.annotate('', xy=(0.5, arrow_end_y), xytext=(0.5, arrow_start_y),
                        arrowprops=dict(arrowstyle="->", color=b["border"], lw=2.0, mutation_scale=15))
            
            # Arrow Text Box (Centered beside arrow with ample space)
            ax.text(0.5, mid_y, f"  {b['arrow_text']}  ", ha='center', va='center', fontsize=8.5, fontweight='bold',
                    color='#475569', bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=b["border"], lw=1.0, alpha=0.95))
            
    ax.set_title('Comparative Application Security Workflow (STSF Causal Engine)', fontsize=13.5, pad=15, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/fig_comparative_workflow.png', dpi=300, bbox_inches='tight', pad_inches=0.15)
    plt.savefig('fig_comparative_workflow.png', dpi=300, bbox_inches='tight', pad_inches=0.15)
    plt.close()

# -------------------------------------------------------------------
# 2. Figure 10 — Security Model Comparison (Block-by-Block)
# -------------------------------------------------------------------
def generate_block_model_comp():
    fig, ax = plt.subplots(figsize=(9.5, 6.5), dpi=300)
    ax.axis('off')
    
    # Left Box: Sheikh Model
    left_x = 0.05
    box_w = 0.42
    
    # Title Left
    rect_l_head = patches.FancyBboxPatch(
        (left_x, 0.80), box_w, 0.12,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        fc="#e0f2fe", ec="#0284c7", lw=1.8
    )
    ax.add_patch(rect_l_head)
    ax.text(left_x + box_w/2, 0.86, "Sheikh et al. Target Attack Model\n(Single Target Expected Value P_TA)", 
            ha='center', va='center', fontweight='bold', fontsize=11, color="#0369a1")
    
    # Content Left
    rect_l_body = patches.FancyBboxPatch(
        (left_x, 0.10), box_w, 0.66,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        fc="#f8fafc", ec="#cbd5e1", lw=1.5
    )
    ax.add_patch(rect_l_body)
    
    left_text = (
        "1. Model Definition:\n"
        "   Evaluates single-subsystem target attack\n"
        "   probability P_TA = (2P_SA + P_SCADA + P_R) / 4\n\n"
        "2. Centralized Baseline (Without BC):\n"
        "   P_TA = 0.0050  (0.5% Expected Risk)\n\n"
        "3. Decentralized BFT (With BC):\n"
        "   P_TAb ≈ 4.91 × 10⁻¹⁷³  (Static Gain)\n\n"
        "4. Key Limitation:\n"
        "   Assumes attacker targets 1 random subsystem.\n"
        "   Does not evaluate parallel multi-vector ingress."
    )
    ax.text(left_x + 0.03, 0.43, left_text, ha='left', va='center', fontsize=9.5, color="#1e293b", linespacing=1.5)
    
    # Right Box: Parallel Model
    right_x = 0.53
    
    # Title Right
    rect_r_head = patches.FancyBboxPatch(
        (right_x, 0.80), box_w, 0.12,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        fc="#f3e8ff", ec="#9333ea", lw=1.8
    )
    ax.add_patch(rect_r_head)
    ax.text(right_x + box_w/2, 0.86, "Parallel System Compromise Model\n(Worst-Case Series Ingress P_Compromise)", 
            ha='center', va='center', fontweight='bold', fontsize=11, color="#6b21a8")
    
    # Content Right
    rect_r_body = patches.FancyBboxPatch(
        (right_x, 0.10), box_w, 0.66,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        fc="#f8fafc", ec="#cbd5e1", lw=1.5
    )
    ax.add_patch(rect_r_body)
    
    right_text = (
        "1. Model Definition:\n"
        "   Evaluates 12 parallel cyber-physical attack\n"
        "   vectors P_Compromise = 1 - ∏(1 - P_atk^j)\n\n"
        "2. Centralized Baseline (Without BC):\n"
        "   P_Compromise = 0.9740  (97.4% Vulnerable!)\n\n"
        "3. Decentralized BFT (With BC):\n"
        "   P_Compromise ≈ 5.99 × 10⁻⁷  (0.00006% Risk)\n\n"
        "4. Engineering Insight:\n"
        "   Proves centralized grids are 97.4% compromised\n"
        "   under parallel attacks, reinforcing BFT consensus."
    )
    ax.text(right_x + 0.03, 0.43, right_text, ha='left', va='center', fontsize=9.5, color="#1e293b", linespacing=1.5)
    
    ax.set_title('Security Model Comparison: Single-Target (P_TA) vs. Parallel Failure (P_Compromise)', fontsize=13, pad=15, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/fig_model_comparison.png', dpi=300, bbox_inches='tight', pad_inches=0.15)
    plt.savefig('fig_model_comparison.png', dpi=300, bbox_inches='tight', pad_inches=0.15)
    plt.close()

# -------------------------------------------------------------------
# 3. Figure 0 — Paper Roadmap (Block-by-Block Flowchart)
# -------------------------------------------------------------------
def generate_block_roadmap():
    fig, ax = plt.subplots(figsize=(9.5, 9.0), dpi=300)
    ax.axis('off')
    
    steps = [
        ("1", "1. EV-to-Grid Energy Trading Domain", "Electric Vehicle Integration, AMI Telemetry & Prosumer Energy Market", "#e0f2fe", "#0284c7"),
        ("2", "2. Original Engineering System Limitations", "Centralized Coordinator SPOF (P_SPOF = 1.0), Zero Byzantine Fault Tolerance (f = 0)", "#fee2e2", "#dc2626"),
        ("3", "3. 12-Attack Cyber-Physical Threat Taxonomy", "Physical, Communication, Application & Consensus Layer Attack Surface", "#ffedd5", "#ea580c"),
        ("4", "4. Static-Temporal Security Framework (STSF)", "Analytical Formulation: Static Cryptosystem Gain (10¹⁷⁰) + Poisson Latency Exposure", "#fef3c7", "#d97706"),
        ("5", "5. Consensus Mechanism Performance Comparison", "Evaluating 9 Protocols across Throughput, Latency, Overhead & P_secure", "#dcfce7", "#16a34a"),
        ("6", "6. Practitioner Deployment Roadmap & Insights", "Operational Selection Decision Tree & 5-Step Smart Grid Implementation", "#f0fdf4", "#15803d")
    ]
    
    y_pos = [0.88, 0.72, 0.56, 0.40, 0.24, 0.08]
    box_height = 0.095
    box_width = 0.84
    box_x = 0.08
    
    for i, (num, title, desc, bg, border) in enumerate(steps):
        y = y_pos[i]
        
        rect = patches.FancyBboxPatch(
            (box_x, y - box_height/2), box_width, box_height,
            boxstyle="round,pad=0.01,rounding_size=0.02",
            fc=bg, ec=border, lw=1.8
        )
        ax.add_patch(rect)
        
        badge_size = 0.06
        badge = patches.FancyBboxPatch(
            (box_x + 0.02, y - badge_size/2), badge_size, badge_size,
            boxstyle="round,pad=0.005,rounding_size=0.01",
            fc=border, ec=border
        )
        ax.add_patch(badge)
        ax.text(box_x + 0.05, y, num, ha='center', va='center', color='white', fontweight='bold', fontsize=12)
        
        ax.text(box_x + 0.10, y + 0.02, title, ha='left', va='center', fontweight='bold', fontsize=11.5, color='#0f172a')
        ax.text(box_x + 0.10, y - 0.02, desc, ha='left', va='center', fontsize=9.5, color='#334155')
        
        if i < 5:
            arrow_start_y = y - box_height/2 - 0.005
            arrow_end_y = y_pos[i+1] + box_height/2 + 0.005
            ax.annotate('', xy=(0.5, arrow_end_y), xytext=(0.5, arrow_start_y),
                        arrowprops=dict(arrowstyle="->", color=border, lw=2.0, mutation_scale=15))
            
    ax.set_title('Figure 0 --- Paper Roadmap & Research Methodology Flowchart', fontsize=13.5, pad=15, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/fig_paper_roadmap.png', dpi=300, bbox_inches='tight', pad_inches=0.15)
    plt.savefig('fig_paper_roadmap.png', dpi=300, bbox_inches='tight', pad_inches=0.15)
    plt.close()

if __name__ == "__main__":
    print("Building block-by-block publication figures in Python without text overlap...")
    generate_block_workflow()
    generate_block_model_comp()
    generate_block_roadmap()
    print("Block-by-block Python diagrams successfully generated!")
