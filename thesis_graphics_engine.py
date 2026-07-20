import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as mpath
import networkx as nx
import seaborn as sns
import numpy as np
from math import pi, exp, comb

# --- PREMIUM IEEE STYLE CONFIGURATION ---
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "Bitstream Vera Serif"],
    "mathtext.fontset": "dejavuserif",
    "font.size": 10.5,
    "axes.titlesize": 12.0,
    "axes.labelsize": 10.5,
    "xtick.labelsize": 9.0,
    "ytick.labelsize": 9.0,
    "legend.fontsize": 9.0,
    "lines.linewidth": 1.5,
    "axes.linewidth": 0.8,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linewidth": 0.5,
})

# Royal Blue, Slate Gray, Crimson, Teal, Amber
COLORS = {
    'primary': '#00539F',   # IEEE Blue
    'secondary': '#E74C3C', # Crimson
    'accent1': '#1ABC9C',   # Teal
    'accent2': '#F39C12',   # Amber
    'dark': '#2C3E50',      # Slate Dark
    'light': '#ECF0F1',     # Soft Gray
    'bg': '#FFFFFF'
}

FIGURE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures", "premium")
os.makedirs(FIGURE_DIR, exist_ok=True)

def draw_shadow(ax, x, y, w, h, offset=0.05, alpha=0.15):
    shadow = patches.Rectangle((x+offset, y-offset), w, h, 
                               facecolor='black', alpha=alpha, zorder=0,
                               transform=ax.transData)
    ax.add_patch(shadow)

# -----------------------------------------------------------------
# 1. AMI ARCHITECTURE (Comparison)
# -----------------------------------------------------------------
def draw_ami_architecture():
    print("Generating Premium AMI Architecture...")
    fig, ax = plt.subplots(figsize=(10.0, 5.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis('off')
    
    # Background Panels
    panel_left = patches.Rectangle((0.2, 0.2), 4.6, 6.1, facecolor='#F9F9F9', edgecolor='#BDC3C7', linewidth=1.5, ls='--', zorder=0)
    panel_right = patches.Rectangle((5.2, 0.2), 4.6, 6.1, facecolor='#F9F9F9', edgecolor='#BDC3C7', linewidth=1.5, ls='--', zorder=0)
    ax.add_patch(panel_left)
    ax.add_patch(panel_right)
    
    ax.text(2.5, 6.0, "A. Reactive Centralized IDS", ha='center', weight='bold', color=COLORS['dark'], fontsize=12)
    ax.text(7.5, 6.0, "B. Proactive Distributed BFT", ha='center', weight='bold', color=COLORS['dark'], fontsize=12)
    
    # Utility function for blocks
    def draw_node(x, y, w, h, title, sub, color, edge):
        draw_shadow(ax, x, y, w, h)
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", 
                                      facecolor=color, edgecolor=edge, linewidth=1.5, zorder=2)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2 + 0.15, title, ha='center', va='center', weight='bold', color='#111111', fontsize=9, zorder=3)
        ax.text(x + w/2, y + h/2 - 0.2, sub, ha='center', va='center', color='#333333', fontsize=8, zorder=3)
        
    def draw_arrow(x1, y1, x2, y2, color='#34495E'):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>,head_length=0.6,head_width=0.3", color=color, lw=1.5), zorder=1)
    
    # Left Side: Centralized IDS
    draw_node(0.7, 4.5, 3.6, 0.8, "Smart Meter Tier", "Measures & Forwards Data", '#E8F6F3', '#1ABC9C')
    draw_arrow(2.5, 4.4, 2.5, 3.4)
    draw_node(0.7, 2.5, 3.6, 0.8, "IDS Detection Engine", "SVM + TFPG Classification", '#FDEBD0', '#F39C12')
    draw_arrow(2.5, 2.4, 2.5, 1.4, color=COLORS['secondary'])
    draw_node(0.7, 0.5, 3.6, 0.8, "MDMS / Coordinator (SPOF)", "Alerts processed reactively", '#FADBD8', COLORS['secondary'])
    
    # Right Side: Distributed BFT
    draw_node(5.7, 4.5, 3.6, 0.8, "Smart Meter Tier", "Signs & Hashes Data (PKI)", '#E8F6F3', '#1ABC9C')
    draw_arrow(7.5, 4.4, 7.5, 3.4)
    draw_node(5.7, 2.5, 3.6, 0.8, "Distributed Data Concentrators", "Pre-validates Signatures (P2P)", '#EBF5FB', COLORS['primary'])
    draw_arrow(7.5, 2.4, 7.5, 1.4)
    draw_node(5.7, 0.5, 3.6, 0.8, "BFT Consensus Committee", "Proactive state agreement", '#D4E6F1', COLORS['primary'])
    
    # Connecting the SPOF issue
    ax.text(2.8, 1.95, "Compromise =\nNetwork Fall", ha='left', va='center', color=COLORS['secondary'], fontsize=9, weight='bold')
    ax.text(7.8, 1.95, "Tolerates\nf=16 faults", ha='left', va='center', color=COLORS['primary'], fontsize=9, weight='bold')
    
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURE_DIR, "fig_1_architecture.pdf"), bbox_inches='tight')
    fig.savefig(os.path.join(FIGURE_DIR, "fig_1_architecture.png"), dpi=300, bbox_inches='tight')
    plt.close(fig)

# -----------------------------------------------------------------
# 2. SEQUENCE FLOW (PROTOCOL)
# -----------------------------------------------------------------
def draw_protocol_flow():
    print("Generating Protocol Sequence Flow...")
    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    
    nodes = [("Client\n(Smart Meter)", 1), ("Primary\n(Leader)", 4), ("Replica 1", 6.5), ("Replica 2", 9)]
    for name, x in nodes:
        ax.plot([x, x], [6, 0.5], color=COLORS['dark'], ls='--', lw=1.2, zorder=1)
        ax.text(x, 6.3, name, ha='center', va='center', weight='bold', bbox=dict(facecolor=COLORS['light'], edgecolor=COLORS['dark'], boxstyle='round,pad=0.5'))
        
    def seq_arrow(x1, y1, x2, y2, text, color=COLORS['primary']):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>,head_length=0.5,head_width=0.2", color=color, lw=1.5), zorder=2)
        ax.text((x1+x2)/2, (y1+y2)/2 + 0.15, text, ha='center', color=color, fontsize=8)

    # 1. Request
    seq_arrow(1, 5.5, 4, 5.2, "REQUEST(m, t, c)", color=COLORS['dark'])
    
    # 2. Pre-Prepare
    seq_arrow(4, 5.0, 6.5, 4.7, "PRE-PREPARE")
    seq_arrow(4, 5.0, 9, 4.4, "PRE-PREPARE")
    
    # 3. Prepare
    seq_arrow(6.5, 4.2, 4, 3.9, "PREPARE")
    seq_arrow(6.5, 4.2, 9, 3.6, "PREPARE")
    seq_arrow(9, 4.0, 4, 3.7, "PREPARE")
    seq_arrow(9, 4.0, 6.5, 3.4, "PREPARE")
    
    # 4. Commit
    seq_arrow(4, 3.0, 6.5, 2.7, "COMMIT", color=COLORS['accent1'])
    seq_arrow(4, 3.0, 9, 2.4, "COMMIT", color=COLORS['accent1'])
    seq_arrow(6.5, 2.8, 4, 2.5, "COMMIT", color=COLORS['accent1'])
    seq_arrow(9, 2.6, 4, 2.3, "COMMIT", color=COLORS['accent1'])
    
    # 5. Reply
    seq_arrow(4, 1.5, 1, 1.2, "REPLY", color=COLORS['dark'])
    seq_arrow(6.5, 1.5, 1, 0.9, "REPLY", color=COLORS['dark'])
    seq_arrow(9, 1.5, 1, 0.6, "REPLY", color=COLORS['dark'])
    
    # Annotations
    ax.text(10, 5.5, "Client Phase", color=COLORS['dark'], va='center', fontsize=9, style='italic')
    ax.text(10, 4.7, "Pre-Prepare Phase", color=COLORS['primary'], va='center', fontsize=9, style='italic')
    ax.text(10, 3.8, "Prepare Phase\n(Verify)", color=COLORS['primary'], va='center', fontsize=9, style='italic')
    ax.text(10, 2.7, "Commit Phase\n(Finalize)", color=COLORS['accent1'], va='center', fontsize=9, style='italic')
    
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURE_DIR, "fig_2_protocol_flow.pdf"), bbox_inches='tight')
    fig.savefig(os.path.join(FIGURE_DIR, "fig_2_protocol_flow.png"), dpi=300, bbox_inches='tight')
    plt.close(fig)

if __name__ == '__main__':
    draw_ami_architecture()
    draw_protocol_flow()
# -----------------------------------------------------------------
# 3. PROBABILITY TREE (Attack Graph)
# -----------------------------------------------------------------
def draw_probability_tree():
    print("Generating Probability Tree...")
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.axis('off')
    
    # We will use networkx for tree layout
    G = nx.DiGraph()
    nodes = {
        "Root": (0, 0),
        "IDS(0)": (2, 2),
        "IDS(1)": (2, -2),
        "BFT(0)": (4, 3),
        "BFT(1)": (4, 1),
        "SPOF(0)": (4, -1),
        "SPOF(1)": (4, -3),
    }
    
    labels = {
        "Root": "Initial State",
        "IDS(0)": "IDS Detects (1-P_IDS)",
        "IDS(1)": "IDS Misses (P_IDS)",
        "BFT(0)": "Consensus Prevents\n(P_Byz < 1)",
        "BFT(1)": "Consensus Fails\n(P_Byz = 1)",
        "SPOF(0)": "SPOF Intact",
        "SPOF(1)": "SPOF Compromised\n(System Fails)"
    }
    
    edges = [
        ("Root", "IDS(0)", "P_detect"), ("Root", "IDS(1)", "P_IDS"),
        ("IDS(0)", "BFT(0)", "1-P_Byz"), ("IDS(0)", "BFT(1)", "P_Byz"),
        ("IDS(1)", "SPOF(0)", "1-P_c"), ("IDS(1)", "SPOF(1)", "P_c")
    ]
    
    for u, v, lbl in edges:
        G.add_edge(u, v, label=lbl)
        
    for node, pos in nodes.items():
        color = COLORS['primary'] if '0' in node else COLORS['secondary']
        if node == "Root": color = COLORS['dark']
        
        # Node circles
        circle = patches.Circle(pos, radius=0.4, facecolor=color, edgecolor='#222', alpha=0.9, zorder=2)
        ax.add_patch(circle)
        
        # Node Labels
        ax.text(pos[0], pos[1] + 0.6, labels[node], ha='center', va='center', fontsize=9, weight='bold')

    for u, v, lbl in edges:
        p1, p2 = nodes[u], nodes[v]
        ax.annotate("", xy=p2, xytext=p1,
                    arrowprops=dict(arrowstyle="->", color='#555', lw=1.5, shrinkA=15, shrinkB=15), zorder=1)
        ax.text((p1[0]+p2[0])/2, (p1[1]+p2[1])/2 + 0.2, lbl, ha='center', color=COLORS['dark'], fontsize=8)

    fig.tight_layout()
    fig.savefig(os.path.join(FIGURE_DIR, "fig_3_probability_tree.pdf"), bbox_inches='tight')
    fig.savefig(os.path.join(FIGURE_DIR, "fig_3_probability_tree.png"), dpi=300, bbox_inches='tight')
    plt.close(fig)

# -----------------------------------------------------------------
# 4. RADAR CHART COMPARISON
# -----------------------------------------------------------------
def draw_radar_comparison():
    print("Generating Radar Chart Comparison...")
    labels = np.array(['Throughput', 'Latency', 'Security (Byzantine Tolerant)', 'Message Complexity', 'Decentralization'])
    num_vars = len(labels)
    
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]
    
    # Normalized scores (0-10)
    pbft = [6, 4, 10, 3, 5]
    tbft = [8, 8, 10, 8, 8]
    rvr  = [9, 9, 8,  9, 9]
    ids  = [10, 10, 1, 10, 1]
    
    pbft += pbft[:1]
    tbft += tbft[:1]
    rvr += rvr[:1]
    ids += ids[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    
    def plot_radar(data, color, label):
        ax.plot(angles, data, color=color, linewidth=2, label=label)
        ax.fill(angles, data, color=color, alpha=0.1)
        
    plot_radar(ids, COLORS['secondary'], 'Reactive IDS (Baseline)')
    plot_radar(pbft, COLORS['dark'], 'Classic PBFT')
    plot_radar(tbft, COLORS['primary'], 'Tower BFT')
    plot_radar(rvr, COLORS['accent1'], 'RVR Consensus')
    
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_ylim(0, 10)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURE_DIR, "fig_4_radar_comparison.pdf"), bbox_inches='tight')
    fig.savefig(os.path.join(FIGURE_DIR, "fig_4_radar_comparison.png"), dpi=300, bbox_inches='tight')
    plt.close(fig)

# -----------------------------------------------------------------
# 5. POISSON TIMELINE
# -----------------------------------------------------------------
def draw_poisson_timeline():
    print("Generating Poisson Timeline...")
    fig, ax = plt.subplots(figsize=(9, 2.5))
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(-1, 2)
    
    # Timeline
    ax.plot([0, 9], [0, 0], color=COLORS['dark'], lw=2, zorder=1)
    ax.annotate("", xy=(9.5, 0), xytext=(9, 0), arrowprops=dict(arrowstyle="->", color=COLORS['dark'], lw=2))
    ax.text(9.7, 0, "Time (t)", va='center', weight='bold')
    
    # Events
    events = [
        (1, "Attack Initiated", COLORS['secondary'], 1),
        (3, "Vulnerability Window ($)", COLORS['accent2'], -1),
        (5, "Consensus Starts", COLORS['primary'], 1),
        (7, "Block Finalized (Latency $)", COLORS['primary'], -1)
    ]
    
    for t, label, color, d in events:
        ax.plot([t, t], [0, d*0.5], color=color, lw=1.5, ls='--')
        ax.plot(t, 0, 'o', color=color, markersize=8, zorder=2)
        ax.text(t, d*0.6, label, ha='center', va='center', color=color, weight='bold', fontsize=9)
        
    # Attack rate poisson arrivals
    arrivals = [1.5, 2.2, 3.8, 4.5, 6.2]
    for a in arrivals:
        ax.plot(a, 0, 'x', color=COLORS['secondary'], markersize=6, zorder=3)
    ax.text(4, -0.3, "Poisson Arrivals ($\lambda$)", color=COLORS['secondary'], ha='center', fontsize=9)
        
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURE_DIR, "fig_5_poisson_timeline.pdf"), bbox_inches='tight')
    fig.savefig(os.path.join(FIGURE_DIR, "fig_5_poisson_timeline.png"), dpi=300, bbox_inches='tight')
    plt.close(fig)

if __name__ == '__main__':
    draw_probability_tree()
    draw_radar_comparison()
    draw_poisson_timeline()

# -----------------------------------------------------------------
# 6. MATHEMATICAL PLOTS (SPOF & SENSITIVITY)
# -----------------------------------------------------------------
def draw_spof_risk():
    print("Generating SPOF Risk Plot...")
    pc_vals = np.linspace(0.01, 0.20, 100)
    p_byz_ids = np.ones_like(pc_vals)
    
    n = 51
    f = 16
    p_byz_bft = []
    for pc in pc_vals:
        val = sum(comb(n, i) * (pc**i) * ((1.0 - pc)**(n - i)) for i in range(f + 1, n + 1))
        p_byz_bft.append(val)
        
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.plot(pc_vals, p_byz_ids, color=COLORS['secondary'], linestyle='--', linewidth=2, label='Centralized IDS (SPOF)')
    ax.plot(pc_vals, p_byz_bft, color=COLORS['primary'], linestyle='-', linewidth=2.5, label='BFT Blockchain (=51, f=16$)')
    
    ax.set_yscale('log')
    ax.set_xlabel('Per-Node Compromise Probability ($)')
    ax.set_ylabel('System Failure Probability ({Byz}$)')
    ax.set_title('SPOF vs. Byzantine Fault Tolerance Risk')
    ax.legend(loc='lower right', frameon=True, shadow=True)
    
    ax.axhline(1e-5, color=COLORS['dark'], linestyle=':', alpha=0.5)
    ax.text(0.02, 2e-5, '^{-5}$ Safety Threshold', color=COLORS['dark'], fontsize=9)
    
    sns.despine()
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURE_DIR, "fig_6_spof_risk.pdf"), bbox_inches='tight')
    fig.savefig(os.path.join(FIGURE_DIR, "fig_6_spof_risk.png"), dpi=300, bbox_inches='tight')
    plt.close(fig)

def draw_sensitivity_sweeps():
    print("Generating Sensitivity Sweeps...")
    def p_temporal_poisson(l_ms, lam, p_ta):
        return 1.0 - exp(-lam * (l_ms/1000.0) * p_ta)
        
    def p_secure(p_s, p_t, rho=0.3):
        p_fail = min(1.0, p_s + p_t - rho * min(p_s, p_t))
        return (1.0 - p_fail) * (1.0 - 0.05)
        
    eta_vals = np.linspace(0.05, 0.25, 50)
    l_pbft, l_tbft, l_rvr = 7650.0, 242.9, 200.0
    
    ps_pbft = [p_secure(1e-172*(1.0-e*0.5), p_temporal_poisson(l_pbft, 20.0, 0.005)) for e in eta_vals]
    ps_tbft = [p_secure(1e-172*(1.0-e*0.5), p_temporal_poisson(l_tbft, 20.0, 0.005)) for e in eta_vals]
    ps_rvr  = [p_secure(1e-172*(1.0-e*0.5), p_temporal_poisson(l_rvr, 20.0, 0.005)) for e in eta_vals]
    
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.plot(eta_vals, ps_pbft, color=COLORS['dark'], label='Classic PBFT', lw=2)
    ax.plot(eta_vals, ps_tbft, color=COLORS['primary'], label='Tower BFT', lw=2)
    ax.plot(eta_vals, ps_rvr, color=COLORS['accent1'], label='RVR Consensus', lw=2.5)
    
    ax.set_xlabel('Spatial Cross-Verification Factor ($\eta$)')
    ax.set_ylabel('Overall Security Probability ({secure}$)')
    ax.set_title('Sensitivity to Spatial Validation Factor ($\eta$)')
    ax.legend(loc='lower right', frameon=True, shadow=True)
    
    sns.despine()
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURE_DIR, "fig_7_eta_sensitivity.pdf"), bbox_inches='tight')
    fig.savefig(os.path.join(FIGURE_DIR, "fig_7_eta_sensitivity.png"), dpi=300, bbox_inches='tight')
    plt.close(fig)

if __name__ == '__main__':
    draw_spof_risk()
    draw_sensitivity_sweeps()

# -----------------------------------------------------------------
# 7. BLOCKCHAIN ARCHITECTURE
# -----------------------------------------------------------------
def draw_blockchain_architecture():
    print("Generating Blockchain Architecture...")
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.axis('off')
    
    # Using NetworkX to create a ring topology for BFT validators
    G = nx.cycle_graph(6)
    pos = nx.circular_layout(G, scale=2.5)
    
    # Shift network to the right
    pos = {i: (p[0] + 6.5, p[1] + 3) for i, p in pos.items()}
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, ax=ax, width=1.5, edge_color=COLORS['dark'], style='--')
    
    # Draw Nodes
    for i, p in pos.items():
        color = COLORS['primary'] if i != 0 else COLORS['accent2'] # i=0 is Leader
        label = "Primary" if i == 0 else f"Replica {i}"
        
        # Shadow & Node
        circle = patches.Circle(p, radius=0.4, facecolor=color, edgecolor=COLORS['dark'], linewidth=1.5, zorder=3)
        ax.add_patch(circle)
        ax.text(p[0], p[1]-0.6, label, ha='center', fontsize=9, weight='bold')

    # Draw Blockchain ledger
    ax.text(6.5, 6.2, "BFT Validator Network", ha='center', fontsize=11, weight='bold', color=COLORS['dark'])
    
    # Draw Client / Smart Meter side
    box_client = patches.FancyBboxPatch((0.5, 2.5), 2.5, 1.0, boxstyle="round,pad=0.1", 
                                        facecolor='#E8F6F3', edgecolor='#1ABC9C', linewidth=1.5)
    ax.add_patch(box_client)
    ax.text(1.75, 3.0, "Smart Meter\n(Client)", ha='center', va='center', weight='bold')
    
    # Mempool
    box_mempool = patches.FancyBboxPatch((3.5, 2.5), 1.5, 1.0, boxstyle="round,pad=0.1", 
                                         facecolor='#FDEBD0', edgecolor='#F39C12', linewidth=1.5)
    ax.add_patch(box_mempool)
    ax.text(4.25, 3.0, "Mempool", ha='center', va='center', weight='bold')
    
    # Arrows
    ax.annotate("", xy=(3.5, 3.0), xytext=(3.0, 3.0), arrowprops=dict(arrowstyle="->", lw=2, color=COLORS['dark']))
    ax.annotate("", xy=(5.0, 3.0), xytext=(4.0, 3.0), arrowprops=dict(arrowstyle="->", lw=2, color=COLORS['dark']))
    
    # Ledger Append
    box_ledger = patches.FancyBboxPatch((5.5, 0.5), 2.0, 0.6, boxstyle="round,pad=0.1", 
                                        facecolor='#EAEDED', edgecolor='#95A5A6', linewidth=1.5)
    ax.add_patch(box_ledger)
    ax.text(6.5, 0.8, "Append to Ledger", ha='center', va='center', weight='bold')
    
    ax.annotate("", xy=(6.5, 1.1), xytext=(6.5, 1.5), arrowprops=dict(arrowstyle="->", lw=2, color=COLORS['primary']))

    fig.tight_layout()
    fig.savefig(os.path.join(FIGURE_DIR, "fig_8_blockchain_arch.pdf"), bbox_inches='tight')
    fig.savefig(os.path.join(FIGURE_DIR, "fig_8_blockchain_arch.png"), dpi=300, bbox_inches='tight')
    plt.close(fig)

if __name__ == '__main__':
    draw_blockchain_architecture()

# -----------------------------------------------------------------
# 8. THREAT MODEL MATRIX & ATTACK GRAPH
# -----------------------------------------------------------------
def draw_threat_model_graph():
    print("Generating Threat Model Attack Graph...")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axis('off')
    
    G = nx.DiGraph()
    # Nodes: [Layer/Type, Risk, X, Y]
    nodes = {
        'Attacker': [0, 2],
        'Physical Tamper': [1.5, 3.5],
        'Network Sniffing': [1.5, 2],
        'Malware Injection': [1.5, 0.5],
        'Smart Meter': [3, 3],
        'Concentrator': [3, 1],
        'MDMS (SPOF)': [5, 2],
        'False Data Injection': [7, 3],
        'Denial of Service': [7, 1],
        'Grid Blackout': [9, 2]
    }
    
    for n in nodes: G.add_node(n)
        
    edges = [
        ('Attacker', 'Physical Tamper'), ('Attacker', 'Network Sniffing'), ('Attacker', 'Malware Injection'),
        ('Physical Tamper', 'Smart Meter'), ('Network Sniffing', 'Smart Meter'), ('Network Sniffing', 'Concentrator'),
        ('Malware Injection', 'Concentrator'), ('Smart Meter', 'MDMS (SPOF)'), ('Concentrator', 'MDMS (SPOF)'),
        ('MDMS (SPOF)', 'False Data Injection'), ('MDMS (SPOF)', 'Denial of Service'),
        ('False Data Injection', 'Grid Blackout'), ('Denial of Service', 'Grid Blackout')
    ]
    G.add_edges_from(edges)
    
    for n, pos in nodes.items():
        color = COLORS['primary']
        if n == 'Attacker': color = COLORS['dark']
        elif 'Grid' in n or 'MDMS' in n: color = COLORS['secondary']
        
        # Add a pill-shape for nodes
        box = patches.FancyBboxPatch((pos[0]-0.8, pos[1]-0.3), 1.6, 0.6, boxstyle="round,pad=0.1", 
                                      facecolor=color, edgecolor='#222', lw=1.5, zorder=3)
        draw_shadow(ax, pos[0]-0.8, pos[1]-0.3, 1.6, 0.6, alpha=0.1)
        ax.add_patch(box)
        
        # Wrap text
        txt = n.replace(' ', '\n')
        ax.text(pos[0], pos[1], txt, ha='center', va='center', weight='bold', color='white', fontsize=8, zorder=4)

    for u, v in edges:
        p1, p2 = nodes[u], nodes[v]
        # Calculate intersection with edge of pill
        ax.annotate("", xy=(p2[0]-0.9, p2[1]), xytext=(p1[0]+0.9, p1[1]),
                    arrowprops=dict(arrowstyle="->", color=COLORS['dark'], lw=1.5), zorder=1)
                    
    ax.set_title("Twelve-Attack Threat Vector Graph (IDS Vulnerability)", weight='bold')

    fig.tight_layout()
    fig.savefig(os.path.join(FIGURE_DIR, "fig_9_attack_graph.pdf"), bbox_inches='tight')
    fig.savefig(os.path.join(FIGURE_DIR, "fig_9_attack_graph.png"), dpi=300, bbox_inches='tight')
    plt.close(fig)

# -----------------------------------------------------------------
# 9. RESEARCH METHODOLOGY WORKFLOW
# -----------------------------------------------------------------
def draw_workflow_pipeline():
    print("Generating Research Methodology Pipeline...")
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.axis('off')
    
    stages = [
        ("Analytical Modeling\n(Phase 1)", "Math Formulation\n(Probability & Reliability)"),
        ("Simulation Framework\n(Phase 2)", "NS3 & Hyperledger\n(Python Prototyping)"),
        ("Experimental Evaluation\n(Phase 3)", "Metrics Collection\n(Latency, Throughput, P_Byz)"),
        ("Comparative Analysis\n(Phase 4)", "Benchmarking IDS vs.\nPBFT vs. Tower vs. RVR")
    ]
    
    for i, (title, sub) in enumerate(stages):
        x = i * 2.5
        box = patches.FancyBboxPatch((x, 1), 2.0, 1.0, boxstyle="round,pad=0.1", 
                                      facecolor=COLORS['light'], edgecolor=COLORS['dark'], lw=1.5, zorder=2)
        ax.add_patch(box)
        
        ax.text(x + 1.0, 1.6, title, ha='center', va='center', weight='bold', color=COLORS['primary'], fontsize=9)
        ax.text(x + 1.0, 1.3, sub, ha='center', va='center', color=COLORS['dark'], fontsize=8)
        
        if i < len(stages) - 1:
            ax.annotate("", xy=(x + 2.5, 1.5), xytext=(x + 2.0, 1.5),
                        arrowprops=dict(arrowstyle="-|>,head_length=0.6,head_width=0.3", color=COLORS['secondary'], lw=2), zorder=1)

    fig.tight_layout()
    fig.savefig(os.path.join(FIGURE_DIR, "fig_10_methodology_pipeline.pdf"), bbox_inches='tight')
    fig.savefig(os.path.join(FIGURE_DIR, "fig_10_methodology_pipeline.png"), dpi=300, bbox_inches='tight')
    plt.close(fig)

if __name__ == '__main__':
    draw_threat_model_graph()
    draw_workflow_pipeline()
