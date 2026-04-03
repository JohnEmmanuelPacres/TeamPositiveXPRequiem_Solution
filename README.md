# Team PositiveXPRequiem | A.S.T.R.A Framework

**START-DOST Hackathon Solution: Decision Support System (DSS)**

This project is a professional-grade predictive Decision Support System (DSS) designed to track, analyze, and mitigate structural risks—specifically **out-of-field teaching**—in the Philippine science and mathematics education sector.

By unifying fragmented data, the **A.S.T.R.A** framework acts as a mathematical playbook for strategic resource allocation, leveraging **Prescriptive Intelligence** to heal educational vulnerabilities system-wide.

## Hackathon Highlights & Core Features

- **Longitudinal Timeframe Simulator (2022-2026):** Algorithmically reverse-engineers historical datasets using dynamic XP penalties to simulate programmatic ROI and Year-Over-Year (YoY) recovery metrics.
- **Prescriptive Intelligence (AI Clustering):** Uses `scikit-learn` K-Means clustering to segment the workforce into dynamic capability cohorts ("Novice Pool", "Core Tier", "Veteran Legends").
- **Gamified Teacher UX (Role-Based Access):** Features an engaging RPG-inspired interface for end-users, visualizing capabilities via Plotly "Skill-Tree" Radar Charts and dynamically matching them with "Local Legends" for mentorship.
- **Geospatial Macro-Routing:** A Project NOAH-style 3D logistics map powered by `pydeck` that calculates supply-and-demand to route mentors from robust regional hubs inward to underserved epicenters.
- **Obsidian Mentorship Graph:** Interactive node topology displaying mentor-mentee connectivity via `NetworkX` and `pyvis`.

## Architecture Overview

The system operates as a Modular Monolith in Python, running fully local to simulate high-end prescriptive analytics while guaranteeing performance on low-end hardware.

The platform is divided into Four Core Pillars:

1. **Pillar 1: Geospatial Tracker**: Project NOAH-style 3D logistics and K-Means hub displacement maps.
2. **Pillar 2: Ingestion Engine**: String normalization ('Schema Healer') utility mapped using `thefuzz[speedup]` to sanitize incoming datasets natively.
3. **Pillar 3: Network Dashboard**: Interactive node topology representing organic knowledge-transfer graphs.
4. **Pillar 4: Intelligence Hub**: Real-time math algorithms calculating local Fragility Scores and 2D Cohort Heatmaps for macro-admin oversight.

## Methodology & Mathematical Formalization

While the ultimate vision for A.S.T.R.A explores Graph Neural Networks (GNN) for predictive peer-to-peer vulnerability modeling, the current computational architecture uses a **Deterministic Graph Heuristic** and **K-Means Clustering**. This ensures 100% computational transparency (Explainable AI) suitable for government compliance, while perfectly simulating the topological mapping required for future GNN integration.

### 1. The Fragility Index

The vulnerability of a teacher node is assessed via a weighted heuristic function penalizing out-of-field teaching and lack of experience:

$$
F(n) = w_1(M_n) + w_2(e^{-\lambda X_n}) + w_3(R_{c})
$$

_Where:_

- $F(n)$ = Vulnerability of teacher $n$
- $M_n$ = Binary out-of-field mismatch penalty (Subject vs. Major Specialization)
- $X_n$ = Years of experience (decaying penalty)
- $R_c$ = Regional capacity penalty

### 2. Workforce Clustering (K-Means)

Cohorts mathematically minimize variance across the workforce. The model maps features $X = [Age, Experience]$ and minimizes the within-cluster sum of squares to dynamically classify boundaries between the "Novice Pool" and the "Veteran Legends":

$$
J = \sum_{j=1}^{k} \sum_{i=1}^{n} ||x_i - \mu_j||^2
$$

### 3. Stochastic Degradation Model (Timeframe Simulator)

The longitudinal tracking dynamically reverse-engineers datasets to simulate programmatic ROI over a closed-system cohort:

$$
E_{past} = \max(0, E_{current} - \Delta t - \epsilon)
$$

_Where:_ $\epsilon$ is stochastic noise ($\mathcal{N}$) injected to simulate the uneven, volatile historical capability distributions present prior to A.S.T.R.A framework interventions.

## Prerequisites

- **Python**: version 3.8+ recommended.

## Installation

We highly recommend running this solution inside a Python virtual environment to avoid native library conflicts (if you opt to use docker instead of virtual environment, scroll down to 'Using Docker' section).

1. **Create and Activate a Virtual Environment:**

   _Windows:_

   ```bash
   python -m venv venv
   .\venv\Scripts\activate

   or

   source venv/Scripts/activate
   ```

   _macOS / Linux:_

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Dashboard

### Local Native Execution

Once all dependencies are installed, initialize the Streamlit server from the application root:

```bash
streamlit run main.py
```

The system will start locally. Navigate to http://localhost:8501 inside your web browser.

### Using Docker

For isolated containerized execution, you can build and run the app via Docker.

1. **Build the Image**

   ```bash
   docker build -t positivexprequiem-dss .
   ```

2. **Run the Container**
   ```bash
   docker run -d -p 8501:8501 --name dss_dashboard positivexprequiem-dss
   ```

Navigate to http://localhost:8501 in your web browser.

## Data Constraints

This prototype securely leverages an in-memory Pandas dataframe cloned from `Dataset/Data/STAR_Integrated_Data*.csv`. Standard deployments in the simulator module update visual Streamlit session-state cache buffers exclusively and **DO NOT modify or mutate** the source CSV data internally.
