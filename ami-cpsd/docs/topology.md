# Smart Grid Topology & Graph Formulation

## 1. Network Hierarchy Structure

The AMI infrastructure is organized as a 5-tier spatial graph:

$$\text{Substation (SUB)} \longrightarrow \text{Feeder (FDR)} \longrightarrow \text{Transformer (XFRM)} \longrightarrow \text{NAN} \longrightarrow \text{Smart Meter (SM)}$$

---

## 2. Spatial Distance & Line Impedance

Distance $d_{i,j}$ between smart meter $i$ and meter $j$:

$$d_{i,j} = \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2} \quad [\text{meters}]$$

Feeder line electrical impedance:

$$Z_{i,j} = R_{i,j} + j X_{i,j} = (0.0005 \cdot d_{i,j}) + j(0.0002 \cdot d_{i,j}) \quad [\Omega]$$

This graph topology is exported to `nodes.csv` and `edges.csv` for Graph Neural Network (GNN) models.
