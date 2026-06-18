 # Testing BFT Throughput & Latency: International Standards & Practical Roadmap
 
 ## TL;DR — What Standards Exist?
 
 There is **no single ISO or IEEE standard** that defines exact TPS/latency benchmarks for blockchain consensus. Instead, the landscape is a **layered ecosystem** of vocabulary standards, testing frameworks, and open-source benchmark tools. Here's the full picture:
 
 | Standard / Tool | Organization | What It Covers | Status |
 |---|---|---|---|
 | **ISO 22739** | ISO/TC 307 | Vocabulary & definitions for blockchain/DLT | Published (2020, rev. 2024) |
 | **ISO 23257** | ISO/TC 307 | Reference architecture for DLT systems | Published (2022) |
 | **ISO 22739-2** | ISO/TC 307 | Extended vocabulary including performance terms | Under development |
 | **IEEE P3214** | IEEE BDLSC | Testing specification for blockchain systems (performance, functional, security, stability) | Draft D4.1 (March 2024) |
 | **Hyperledger Caliper** | Linux Foundation | Open-source blockchain performance benchmark tool | Active, production-ready |
 | **BLOCKBENCH** | Dinh et al. (NUS, 2017) | Academic benchmark framework for private blockchains | Published, GitHub available |
 | **TPC-DLT** | Transaction Processing Performance Council | Proposed adaptation of TPC-C/DS for DLT workloads | Conceptual/proposed |
 
 > [!IMPORTANT]
 > The key takeaway: since there is no single "pass/fail" standard, your report should state which framework/methodology you follow, and compare against **published resul
<truncated 13254 bytes>
tion to LaTeX report | ~30 min | Aligns with IEEE P3214 |
 | Cite ISO 22739 vocabulary definitions in your report | ~10 min | International standards compliance |
 
 ### What Would Require New Infrastructure
 
 | Action | Effort | Impact |
 |---|---|---|
 | Deploy 51-node Hyperledger Fabric with SmartBFT | ~1–2 weeks | Caliper-grade production benchmark |
 | Run BLOCKBENCH DoNothing/SmallBank workloads | ~1 week | Academic gold standard comparison |
 | Deploy on AWS/GCP for WAN-realistic testing | ~3–5 days | Real network delay validation |
 
 > [!TIP]
 > For a research project report submitted to an IEEE mentor, **Tier 1 + Tier 2 is sufficient and standard practice.** The reference papers themselves (G-PBFT, SV-PBFT, RVR) all used custom simulators, not Caliper. Only CE-PBFT used an actual blockchain platform.
 
 ---
 
 ## Key References to Cite
 
 ```bibtex
 @inproceedings{dinh2017blockbench,
   title     = {{BLOCKBENCH}: A Framework for Analyzing Private Blockchains},
   author    = {Dinh, T. T. A. and Wang, J. and Chen, G. and others},
   booktitle = {Proc. ACM SIGMOD},
   year      = {2017},
   pages     = {1085--1100}
 }
 
 @misc{caliper2023,
   title     = {Hyperledger Caliper},
   author    = {{Hyperledger Foundation}},
   year      = {2023},
   url       = {https://hyperledger.github.io/caliper/}
 }
 
 @standard{iso22739,
   title     = {Blockchain and distributed ledger technologies --- Vocabulary},
   number    = {ISO 22739:2020},
   year      = {2020},
   publisher = {International Organization for Standardization}
 }
 
 @standard{ieeep3214,
   title     = {Standard for Testing Specification of Blockchain Systems},
   number    = {IEEE P3214 (Draft)},
   year      = {2024},
   publisher = {IEEE Computer Society BDLSC}
 }
 ```
 
The above content shows the entire, complete file contents of the requested file.
