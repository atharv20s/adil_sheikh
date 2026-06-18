 # BFT Consensus Comparison & LaTeX Report Walkthrough (Purely Analytical Model)
 
 This document provides a comprehensive walkthrough of the comparative analysis of Byzantine Fault Tolerant (BFT) consensus algorithms for secured Electric Vehicle (EV) energy trading on smart grids. It details the comparative results, the real-world paper calibrations, international standards alignment, and the enhancements made to the final LaTeX report. All results are derived from closed-form probabilistic and network complexity equations, with zero Monte Carlo simulation dependency.
 
 ---
 
 ## 1. The 9 BFT Consensus Protocols Evaluated
 
 We evaluated **nine** consensus protocols across **four evolutionary groups** under the unified **Static-Temporal Security Framework (STSF)**:
 
 ### Group 1: Classical Full-Mesh Byzantine Agreement (CFM-BA)
 *   **Lamport OM($m$) [baseline]**: The original recursive oral message protocol.
 *   **Classic PBFT**: The foundational three-phase BFT protocol ($\mathcal{O}(n^2)$ message complexity).
 
 ### Group 2: Committee-Delegated Consortium Consensus (CDC-C)
 *   **IBFT 2.0**: Enterprise quorum-based protocol (used in Hyperledger Besu).
 *   **QBFT**: Optimized IBFT with message piggybacking and faster view changes.
 
 ### Group 3: Hierarchical Topologically-Clustered PBFT (HTC-PBFT)
 *   **CE-PBFT (Ding et al., 2024)**: Credit-evaluation-based node classification.
 *   **G-PBFT (Xu et5 al., 2025)**: Geohash-based clustering with reputation routing.
 *   **SV-P
<truncated 4829 bytes>
nitions (Commit Latency, Read/Write Throughput, and Transaction Success Rates).
 
 ---
 
 ## 5. LaTeX Report Enhancements (`bft_comparison_report.tex`)
 
 We supercharged [bft_comparison_report.tex](file:///c:/Users/athar/OneDrive/Desktop/vjti-comparison-bft-towerbft/bft_comparison_report.tex) by integrating the generated analytical plots using LaTeX `figure` environments, resolving all textual references:
 
 *   **Sheikh baseline plots**: Added replicates of Sheikh's static attack probability curves **without blockchain** (Fig.~15) and **with blockchain** (Fig.~16) to Section II.
 *   **Temporal exposure plot**: Added the curves showing security decay versus block time (Fig.~21) to Section III.
 *   **Consensus Performance Matrix**: Added a **double-column figure** (`figure*`) showing a 4-panel analytical performance grid: latency, throughput, temporal exposure ($P_{temporal}$), and overall security ($P_{secure}$).
 *   **Sensitivity Sweep**: Added an analytical figure in Section VIII showing the latency sensitivity to delay sweeps (10 to 500 ms).
 *   **Key Management**: Added the Shamir Secret Sharing threshold signature impact chart in Section IX, showing the exponential reduction in compromise probability.
 
 ---
 
 ## 6. Practical Roadmap: How to Run the Tests Locally
 
 For the guide/mentor, we outline a concrete testing roadmap in [benchmarking_guide.md](file:///C:/Users/athar/.gemini/antigravity-ide/brain/76167d02-2e77-45ac-a561-438f6e9abb4c/benchmarking_guide.md):
 
 *   **Tier 1 (Analytical Validation)**: Closed-form equations computed in `probabilistic_model.py`.
 *   **Tier 2 (Production-Grade Caliper Benchmark)**: Integrating Hyperledger Caliper and binding to Hyperledger Fabric v2.5 with a YAML benchmark config.
 *   **Tier 3 (Academic BLOCKBENCH Framework)**: Running the `DoNothing` and `SmallBank` workloads in C++ on private blockchain networks.
 
The above content shows the entire, complete file contents of the requested file.
