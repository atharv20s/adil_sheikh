import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_diagram():
    # Set up publication-grade styling
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif", "Bitstream Vera Serif"],
        "font.size": 10,
        "axes.linewidth": 0.8,
    })
    
    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Titles for the two lanes
    ax.text(2.25, 5.7, "A. Reactive Centralized IDS Architecture\n(Single Point of Failure)", 
            ha='center', va='center', weight='bold', color='#C0392B', fontsize=11)
    ax.text(7.25, 5.7, "B. Proactive Distributed BFT Architecture\n(Distributed Multi-Validator)", 
            ha='center', va='center', weight='bold', color='#16A085', fontsize=11)
    
    # ── Draw LANE A (IDS) ──
    # Step 1: Smart Meter
    sm_a = patches.FancyBboxPatch((0.5, 4.8), 3.5, 0.6, boxstyle="round,pad=0.03", 
                                  facecolor='#FADBD8', edgecolor='#E74C3C', linewidth=1.2)
    ax.add_patch(sm_a)
    ax.text(2.25, 5.1, "Smart Meter Nodes\n(Measure raw voltages & power packets)", 
            ha='center', va='center', color='#7B241C', fontsize=8.5)
    
    # Arrow 1
    ax.annotate("", xy=(2.25, 3.9), xytext=(2.25, 4.8),
                arrowprops=dict(arrowstyle="->", color='#E74C3C', lw=1.2, shrinkA=0, shrinkB=0))
    
    # Step 2: SVM & TFPG
    svm_tfpg = patches.FancyBboxPatch((0.5, 3.0), 3.5, 0.9, boxstyle="round,pad=0.03", 
                                      facecolor='#FDEDEC', edgecolor='#EC7063', linewidth=1.2)
    ax.add_patch(svm_tfpg)
    ax.text(2.25, 3.45, "Stage 1: SVM Classifier\n(CPU/RAM Anomaly Detection)\n\nStage 2: TFPG Edit Distance\n(Signature Verification)", 
            ha='center', va='center', color='#7B241C', fontsize=7.5)
    
    # Arrow 2
    ax.annotate("", xy=(2.25, 2.2), xytext=(2.25, 3.0),
                arrowprops=dict(arrowstyle="->", color='#E74C3C', lw=1.2, shrinkA=0, shrinkB=0))
    
    # Step 3: Central MDMS Coordinator (SPOF!)
    mdms = patches.FancyBboxPatch((0.5, 1.3), 3.5, 0.9, boxstyle="round,pad=0.03", 
                                  facecolor='#F1948A', edgecolor='#C0392B', linewidth=1.5)
    ax.add_patch(mdms)
    ax.text(2.25, 1.75, "Central MDMS Coordinator\n(Aggregates alerts & responds)\n\n[CRITICAL SPOF: P_Byz = 1.0]", 
            ha='center', va='center', color='#641E16', weight='bold', fontsize=8.5)
    
    # Arrow 3
    ax.annotate("", xy=(2.25, 0.9), xytext=(2.25, 1.3),
                arrowprops=dict(arrowstyle="->", color='#E74C3C', lw=1.2, shrinkA=0, shrinkB=0))
    
    # Step 4: Reactive alert
    alert = patches.FancyBboxPatch((0.5, 0.1), 3.5, 0.8, boxstyle="round,pad=0.03", 
                                   facecolor='#EAEDED', edgecolor='#95A5A6', linewidth=1.0)
    ax.add_patch(alert)
    ax.text(2.25, 0.5, "Reactive Defense Action\n(Post-compromise warning issued)", 
            ha='center', va='center', color='#5D6D7E', fontsize=8.5)
    
    # ── Draw LANE B (BFT) ──
    # Step 1: Smart Meter with Signing
    sm_b = patches.FancyBboxPatch((5.5, 4.8), 3.5, 0.6, boxstyle="round,pad=0.03", 
                                  facecolor='#D1F2EB', edgecolor='#1ABC9C', linewidth=1.2)
    ax.add_patch(sm_b)
    ax.text(7.25, 5.1, "Smart Meter Nodes\n(Data signed & hashed with private key)", 
            ha='center', va='center', color='#0E6251', fontsize=8.5)
    
    # Arrow 1
    ax.annotate("", xy=(7.25, 3.9), xytext=(7.25, 4.8),
                arrowprops=dict(arrowstyle="->", color='#1ABC9C', lw=1.2, shrinkA=0, shrinkB=0))
    
    # Step 2: Distributed Validator Network
    validators = patches.FancyBboxPatch((5.5, 3.0), 3.5, 0.9, boxstyle="round,pad=0.03", 
                                        facecolor='#E8F8F5', edgecolor='#48C9B0', linewidth=1.2)
    ax.add_patch(validators)
    ax.text(7.25, 3.45, "P2P Data Concentrator Network\n(Distributed validation of\nsignatures & nonces)\n\n[Prevents Replays & Sybil]", 
            ha='center', va='center', color='#0E6251', fontsize=8.0)
    
    # Arrow 2
    ax.annotate("", xy=(7.25, 2.2), xytext=(7.25, 3.0),
                arrowprops=dict(arrowstyle="->", color='#1ABC9C', lw=1.2, shrinkA=0, shrinkB=0))
    
    # Step 3: BFT Consensus Committee
    bft = patches.FancyBboxPatch((5.5, 1.3), 3.5, 0.9, boxstyle="round,pad=0.03", 
                                  facecolor='#A3E4D7', edgecolor='#16A085', linewidth=1.5)
    ax.add_patch(bft)
    ax.text(7.25, 1.75, "Distributed BFT Consensus\n(Prepare -> Commit voting rounds)\n\n[Tolerates up to f = 16 Byzantine nodes]", 
            ha='center', va='center', color='#0B5345', weight='bold', fontsize=8.5)
    
    # Arrow 3
    ax.annotate("", xy=(7.25, 0.9), xytext=(7.25, 1.3),
                arrowprops=dict(arrowstyle="->", color='#1ABC9C', lw=1.2, shrinkA=0, shrinkB=0))
    
    # Step 4: Proactive Ledger Append
    ledger = patches.FancyBboxPatch((5.5, 0.1), 3.5, 0.8, boxstyle="round,pad=0.03", 
                                     facecolor='#EAEDED', edgecolor='#95A5A6', linewidth=1.0)
    ax.add_patch(ledger)
    ax.text(7.25, 0.5, "Proactive Ledger Append\n(Malicious/failed data rejected\nbefore database record)", 
            ha='center', va='center', color='#5D6D7E', fontsize=8.5)
    
    # Save the figure
    fig.tight_layout()
    figure_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures", "fig_architecture_comparison.png")
    os.makedirs(os.path.dirname(figure_path), exist_ok=True)
    fig.savefig(figure_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated architecture comparison diagram at: {figure_path}")

if __name__ == "__main__":
    draw_diagram()
