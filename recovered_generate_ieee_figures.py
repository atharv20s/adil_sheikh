 """
 generate_ieee_figures.py
 ========================
 IEEE-publication-quality figures replicating Fig 15 & Fig 16 from
 Sheikh et al. (IEEE Access, 2020), plus BFT vs Tower BFT comparison.
 
 Style targets:
   - White background, no colored fills
   - Thin lines (1.0-1.5 pt), no markers on dense curves
   - Arrow annotations with italic labels
   - Axis labels in proper serif font
   - Minimal grid, clean ticks
   - Caption-ready sizing (3.5" single column, 7" double column)
 """
 
 import math
 import os
 import numpy as np
 import matplotlib
 matplotlib.use("Agg")
 import matplotlib.pyplot as plt
 from matplotlib.ticker import MultipleLocator, AutoMinorLocator
 
 # ── IEEE Style Setup ────────────────────────────────────────────
 plt.rcParams.update({
     # Font: Times-like serif (IEEE standard)
     "font.family":        "serif",
     "font.serif":         ["Times New Roman", "DejaVu Serif", "Bitstream Vera Serif"],
     "mathtext.fontset":   "dejavuserif",
     # Font sizes (IEEE: 8pt labels, 9pt axis, 10pt titles)
     "font.size":          9,
     "axes.titlesize":     10,
     "axes.labelsize":     9,
     "xtick.labelsize":    8,
     "ytick.labelsize":    8,
     "legend.fontsize":    7.5,
     # Lines
     "lines.linewidth":    1.2,
     "lines.markersize":   4,
     # Axes
     "axes.linewidth":     0.6,
     "axes.grid":   
<truncated 15070 bytes>
egend(fontsize=6.5, loc="upper left", frameon=True,
                edgecolor="black", fancybox=False, framealpha=1.0)
     ax2.text(0.02, 0.97, "(b) With Blockchain", transform=ax2.transAxes,
              fontsize=8, fontweight="bold", va="top")
 
     ax2.annotate(
         "Blockchain reduces\nattack probability\nby orders of magnitude",
         xy=(0.95, 0.005), xytext=(0.925, 0.20),
         fontsize=5.5, fontstyle="italic", ha="center",
         arrowprops=dict(arrowstyle="->", color="black", lw=0.4)
     )
 
     fig.tight_layout(w_pad=2.0)
     path = os.path.join(FIGURE_DIR, "fig18_without_vs_with_blockchain.png")
     fig.savefig(path)
     plt.close(fig)
     print(f"  [OK] {path}")
     return path
 
 
 # ══════════════════════════════════════════════════════════════════
 # MAIN
 # ══════════════════════════════════════════════════════════════════
 
 if __name__ == "__main__":
     print("=" * 60)
     print("  IEEE-Quality Figure Generator")
     print("  Replicating Fig 15, 16 + BFT vs Tower BFT")
     print("=" * 60)
 
     print("\n-- Fig 15: P_TA without blockchain --")
     fig15_pta_no_blockchain()
 
     print("-- Fig 16: P_TAb with blockchain --")
     fig16_ptab_with_blockchain()
 
     print("-- Fig 17: BFT vs Tower BFT comparison --")
     fig17_bft_vs_tbft()
 
     print("-- Fig 18: Without vs With blockchain (OM vs TBFT) --")
     fig18_combined_scenario()
 
     print("\n" + "=" * 60)
     print("  DONE — 4 IEEE-quality figures in ./figures/")
     print("=" * 60)
 
The above content shows the entire, complete file contents of the requested file.
