# Q-SERIES: Topological Materials Discovery Engine

**Version:** 4.1 (Vacuum Ontology Edition)
**Architecture:** Multi-Agent LLM + Lightweight Python Simulation
**Scope:** Universal High-Temperature Topological Hardware

## 1. Overview
The **Q-Series** is a prompt-engineered, closed-loop computational suite designed to discover novel materials for Topological Quantum Computing (TQC). Unlike traditional screening which starts with chemistry, the Q-Series starts with **Quantum Field Theory (QFT)**—defining the target vacuum entanglement structure (e.g., Non-Abelian String-Nets) and then searching for the atomic lattice that realizes it.

The system operates as a sequential pipeline of five specialized agents (`Q1` through `Q5`), bridging the gap between abstract theoretical physics and executable simulation code.

## 2. The Vacuum Ontology
The Q-Series rejects the "Particle-First" view of standard condensed matter physics. Instead, it adopts the **Topological Knot Ontology** (based on Wen, 2017):
*   **Matter** is a pattern of long-range entanglement in the vacuum.
*   **Particles** (Anyons, Majoranas) are topological **defects** in this entanglement.
*   **Design Goal:** Engineer the vacuum (the material bulk) such that its defects function as robust Qubits at ambient temperatures.

## 3. Node Architecture

### **Q1: THE ARCHITECT (Phase Definition)**
*   **Role:** Translates user intent (e.g., "Room Temp Memory") into rigorous QFT constraints.
*   **Input:** Natural Language Requirements.
*   **Output:** `Optimization_Vector` (JSON). Defines the Target Phase (LRE/SRE), Symmetry Constraints, and Minimum Energy Scales ($E_{gap} > 26$ meV).
*   **Key Logic:** Enforces the "Thermal Floor" to ensure room-temperature operation.

### **Q2: THE MINER (Data Retrieval)**
*   **Role:** Bridges Ontology to Reality. Mines literature and databases for physical proxies of topological order.
*   **Input:** Search Vector from Q1.
*   **Output:** `Candidate_Dataset` (JSON). A standardized list of real-world materials with properties like Band Gap, $T_c$, and Spin-Orbit strength.
*   **Key Logic:** Handles "Dirty Data" and maps physical observables (e.g., "Inverted Band") to ontological labels.

### **Q3: THE NAVIGATOR (Multivariate Optimization)**
*   **Role:** The "Brain." Uses Machine Learning (Gaussian Processes) to navigate the trade-offs between topology, stability, and temperature.
*   **Input:** Q2 Dataset.
*   **Output:** `Pareto_Frontier_Candidates` (JSON). Proposed **N-element Alloy Configurations** (e.g., $Bi_{1.5}Sb_{0.5}Te_{1.8}Se_{1.2}$) predicted to outperform known materials.
*   **Key Logic:** Explores the high-dimensional chemical space using Active Learning (UCB).

### **Q4: THE SIMULATOR (Physics Engine)**
*   **Role:** The "Verification." Generates and executes standalone Python code to calculate the topology of specific candidates.
*   **Input:** Candidate Parameters from Q3.
*   **Output:** `Simulation_Plot` & `Topological_Invariant`.
*   **Key Logic:** **Dependency-Lite**. Uses standard `numpy`/`scipy` to construct effective Hamiltonians (BHZ, Kitaev) and simulate **Defect Geometries** (Edges, Vortices) to reveal Anyons.

### **Q5: THE VALIDATOR (Reality Check)**
*   **Role:** The "Gatekeeper." Audits simulation results against thermodynamic and synthesis constraints.
*   **Input:** Q4 Simulation Data.
*   **Output:** `Go/No-Go Decision` & `Feedback_Gradient`.
*   **Key Logic:** Closes the loop. If a material fails (e.g., trivial topology or unstable), it issues specific instructions to Retrain Q3.

## 4. Operation Protocol

### **Execution Commands**
To operate the suite within an LLM session, use the sequential run commands:

1.  `RUN Q1` $\rightarrow$ Initialize Search Strategy.
2.  `RUN Q2` $\rightarrow$ Retrieve Training Data.
3.  `RUN Q3` $\rightarrow$ Predict Novel Alloys.
4.  `RUN Q4` $\rightarrow$ Simulate Physics (Code Generation).
5.  `RUN Q5` $\rightarrow$ Validate & Iteration.

### **Example Workflow**
> **User:** "Find a room-temperature interconnect material."
> **Q1:** Defines target: SRE Phase (QSHI) with $E_g > 26$ meV.
> **Q2:** Mines Bi/Sb/Te data.
> **Q3:** Predicts $Bi_{4}Br_{4-x}I_x$.
> **Q4:** Generates Python script to calculate edge states of the alloy.
> **Q5:** Confirms edge stability at 300K. Generates Datasheet.

## 5. Technical Dependencies
The system is designed to be **Dependency-Lite** for maximum portability in restricted execution environments (like LLM sandboxes):
*   **Required:** `numpy`, `scipy`, `matplotlib` (Standard Stack).
*   **Mocked/Surrogated:** `kwant` (Replaced by custom Hamiltonian matrices), `pymatgen` (Replaced by geometric approximations).
