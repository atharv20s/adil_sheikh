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
# Applying unified design language, consistent typography, and color palette
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "Bitstream Vera Serif"],
    "mathtext.fontset": "dejavuserif",
    "font.size": 11.0,
    "axes.titlesize": 13.0,
    "axes.titleweight": "bold",
    "axes.labelsize": 11.0,
    "axes.labelweight": "bold",
    "xtick.labelsize": 10.0,
    "ytick.labelsize": 10.0,
    "legend.fontsize": 10.0,
    "legend.frameon": True,
    "legend.edgecolor": "black",
    "legend.fancybox": False,
    "lines.linewidth": 2.0,
    "axes.linewidth": 1.2,
    "axes.grid": True,
    "grid.alpha": 0.4,
    "grid.linewidth": 0.7,
    "grid.linestyle": "--",
    "figure.constrained_layout.use": True, # Ensures identical margins
})

# Unified Color Palette
colors = {
    "primary": "#00539F", # IEEE Blue
    "secondary": "#C8102E", # Deep Red
    "tertiary": "#F6A800", # Amber
    "quaternary": "#00857E", # Teal
    "background": "#F0F0F0", # Light Gray
    "node_fill": "#E6F0FA", # Light Blue
    "node_edge": "#003366", # Dark Blue
}

def setup_figure(figsize=(8, 6)):
    """Creates a standardized figure canvas."""
    fig, ax = plt.subplots(figsize=figsize, dpi=300)
    ax.set_facecolor("white")
    return fig, ax

def generate_radar_chart(output_path):
    categories = ['Latency', 'Throughput', 'Fault Tolerance', 'Energy Efficiency', 'Decentralization', 'Security (12-Attack)']
    N = len(categories)
    
    # Values for different paradigms
    values_ids = [8, 9, 2, 8, 1, 4]
    values_pbft = [4, 5, 7, 3, 4, 8]
    values_tower = [9, 8, 9, 7, 8, 10]
    
    # Repeat first value to close the circular graph
    values_ids += values_ids[:1]
    values_pbft += values_pbft[:1]
    values_tower += values_tower[:1]
    
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True), dpi=300)
    
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    
    plt.xticks(angles[:-1], categories, size=11, fontweight='bold')
    ax.set_rlabel_position(0)
    plt.yticks([2, 4, 6, 8, 10], ["2", "4", "6", "8", "10"], color="grey", size=9)
    plt.ylim(0, 10)
    
    # Plot IDS
    ax.plot(angles, values_ids, linewidth=2.5, linestyle='solid', label="Reactive IDS", color=colors['secondary'])
    ax.fill(angles, values_ids, color=colors['secondary'], alpha=0.15)
    
    # Plot PBFT
    ax.plot(angles, values_pbft, linewidth=2.5, linestyle='dashed', label="Classic PBFT", color=colors['tertiary'])
    
    # Plot Tower BFT
    ax.plot(angles, values_tower, linewidth=3.0, linestyle='solid', label="Tower BFT", color=colors['primary'])
    ax.fill(angles, values_tower, color=colors['primary'], alpha=0.25)
    
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
    
    plt.title("Multi-Dimensional Evaluation: IDS vs BFT", y=1.08)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, format='pdf', bbox_inches='tight')
    plt.close()

def generate_latency_chart(output_path):
    fig, ax = setup_figure(figsize=(10, 6))
    
    nodes = np.array([10, 20, 50, 100, 200, 500])
    
    # Simulated latency in ms
    lat_om = nodes * 150
    lat_pbft = nodes * nodes * 2.5
    lat_tower = np.log2(nodes) * 40
    lat_rvr = np.ones_like(nodes) * 200
    
    ax.plot(nodes, lat_om, marker='o', linestyle='-', color=colors['secondary'], label='G1: OM(m)', markersize=8)
    ax.plot(nodes, lat_pbft, marker='s', linestyle='--', color=colors['tertiary'], label='G1: PBFT', markersize=8)
    ax.plot(nodes, lat_tower, marker='D', linestyle='-', color=colors['primary'], label='G4: Tower BFT', markersize=8)
    ax.plot(nodes, lat_rvr, marker='^', linestyle='-.', color=colors['quaternary'], label='G4: RVR', markersize=8)
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    ax.set_xlabel('Number of Validator Nodes ($n$)')
    ax.set_ylabel('Consensus Latency (ms)')
    ax.set_title('Generational BFT Latency Scaling')
    
    ax.legend(loc='upper left')
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, format='pdf', bbox_inches='tight')
    plt.close()

def generate_architecture_diagram(output_path):
    fig, ax = setup_figure(figsize=(12, 8))
    
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Utility Cloud
    rect_utility = patches.Rectangle((4, 7), 4, 2.5, linewidth=2, edgecolor=colors['primary'], facecolor=colors['node_fill'], alpha=0.9, zorder=2)
    ax.add_patch(rect_utility)
    ax.text(6, 8.25, "Utility Control Center (SCADA)\nMDMS & HES", ha='center', va='center', fontsize=12, fontweight='bold', zorder=3)
    
    # BFT Blockchain Layer
    rect_bft = patches.Rectangle((2, 4), 8, 2, linewidth=2, edgecolor=colors['tertiary'], facecolor='#FFF3E0', alpha=0.9, zorder=2)
    ax.add_patch(rect_bft)
    ax.text(6, 5, "BFT Consensus Validator Network\n(Proactive Security Layer)", ha='center', va='center', fontsize=12, fontweight='bold', zorder=3)
    
    # Smart Meters
    for i in range(5):
        rect_meter = patches.Rectangle((1.5 + i*2, 1), 1, 1.5, linewidth=2, edgecolor=colors['quaternary'], facecolor='#E0F2F1', alpha=0.9, zorder=2)
        ax.add_patch(rect_meter)
        ax.text(2 + i*2, 1.75, f"Meter {i+1}", ha='center', va='center', fontsize=10, fontweight='bold', zorder=3)
        
        # Connections
        ax.annotate("", xy=(6, 4), xytext=(2 + i*2, 2.5), arrowprops=dict(arrowstyle="->", color="black", lw=1.5, ls="--"))

    ax.annotate("", xy=(6, 7), xytext=(6, 6), arrowprops=dict(arrowstyle="<->", color="black", lw=2))
    
    ax.set_title("Proposed BFT Architecture for AMI", fontsize=14, fontweight='bold')
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, format='pdf', bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    out_dir = "thesis/premium"
    print(f"Generating unified premium figures to {out_dir}...")
    generate_radar_chart(f"{out_dir}/fig_4_radar_comparison.pdf")
    generate_latency_chart(f"{out_dir}/fig_7_latency_comparison.pdf")
    generate_architecture_diagram(f"{out_dir}/fig_1_architecture.pdf")
    print("Done!")
