# Team PositiveXPRequiem | A.S.T.R.A Framework

**START-DOST Hackathon Solution: Decision Support System (DSS)**

This project is a professional-grade predictive Decision Support System (DSS) designed to track, analyze, and mitigate structural risks—specifically **out-of-field teaching**—in the Philippine science and mathematics education sector.

By unifying fragmented data, the **A.S.T.R.A** framework acts as a mathematical playbook for strategic resource allocation, leveraging **Prescriptive Intelligence** to heal educational vulnerabilities system-wide.

## Table of Contents

- [Hackathon Highlights & Core Features](#hackathon-highlights--core-features)
- [Architecture Overview](#architecture-overview)
- [Recent Updates & Optimizations](#recent-updates--optimizations)
- [Methodology & Mathematical Formalization](#methodology--mathematical-formalization)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Dashboard](#running-the-dashboard)

## Hackathon Highlights & Core Features

- **Longitudinal Timeframe Simulator (2022-2026):** Algorithmically reverse-engineers historical datasets using dynamic XP penalties to simulate programmatic ROI and Year-Over-Year (YoY) recovery metrics.
- **Prescriptive Intelligence (AI Clustering):** Uses `scikit-learn` K-Means clustering to segment the workforce into dynamic capability cohorts ("Novice Pool", "Core Tier", "Veteran Legends").
- **Gamified Teacher UX (Role-Based Access):** Features an engaging RPG-inspired interface for end-users, visualizing capabilities via Plotly "Skill-Tree" Radar Charts and dynamically matching them with "Local Legends" for mentorship.
- **Geospatial Macro-Routing:** A Project NOAH-style 3D logistics map powered by `pydeck` that calculates supply-and-demand to route mentors from robust regional hubs inward to underserved epicenters.
- **Obsidian Mentorship Graph:** Interactive node topology displaying mentor-mentee connectivity via `NetworkX` and `pyvis`.

## Architecture Overview

The system operates as a **Modular Monolith** built entirely in Python via Streamlit. It runs fully local to execute high-end prescriptive analytics and Machine Learning models while ensuring strict data privacy and guaranteeing performance on standard agency hardware. State management is aggressively optimized using `@st.cache_data` and `@st.cache_resource` for near-instant execution of heavy Data Engineering and ML workflows.

### The Technology Stack

- **Frontend / Application State:** Streamlit (Python UI), Plotly WebGL (`go.Scattergl`), PyVis, and PyDeck.
- **Machine Learning & NLP:** HuggingFace `SentenceTransformers` (`paraphrase-multilingual-MiniLM-L12-v2`) and Helsinki-NLP's `MarianMTModel` for zero-shot Tagalog-to-English translations.
- **Clustering & Data Science:** `scikit-learn` (K-Means), `numpy` (`np.polyfit` for longitudinal time series forecasting), and `pandas`.
- **Topological Networking:** `NetworkX`, rendered via `pyvis` to model teacher-mentor ecosystems organically.

### The Four Core Pillars

1. **Geospatial Tracker (`modules/geospatial_tracker/`)**
   - Functions as the primary logistics controller.
   - Powered by `pydeck` to render Project NOAH-style 3D logistics and K-Means hub displacement maps.
   - Algorithmically plans operational travel routes, directing experts from robust geographical hubs into under-indexed, fragile school epicenter zones.

2. **Ingestion Engine (`modules/ingestion/`)**
   - Serves as the automated "Schema Healer" and ETL pipeline.
   - Leverages local PyTorch NLP models to conduct semantic column mapping and on-the-fly TAG-EN language translations.
   - Instantly normalizes disparate, improperly formatted regional CSVs into the heavily standardized schema required by the tracking algorithms.

3. **Network Dashboard (`modules/network_dashboard/`)**
   - Focuses on the interactive node topology representing theoretical knowledge-transfer between regional educators.
   - Utilizes graph math to isolate the "weakest links" in the local mentor-mentee framework, effectively mitigating the structural weakness caused by the "out-of-field teaching" deficit.

4. **Intelligence Hub (`modules/intelligence/`)**
   - Acts as the macro-admin surveillance suite.
   - Runs deterministic real-time heuristics predicting local "Fragility Scores".
   - Computes dynamic classification cohorts and projects an embedded 5-Year timeline simulation across high-density WebGL scatter layers.

## Recent Updates & Optimizations

To prepare for the final presentation and ensure a seamless, production-ready user experience, several core engine and UI optimizations were recently implemented:

- **Mentorship Ecosystem Overhaul**: Upgraded the _Intelligence Hub_ with sleek UI metric cards and transitioned from standard Plotly overlays to GPU-accelerated **`go.Scattergl`**. This resolved browser lagging issues when visualizing dense cohort demographic scatter plots.
- **Micro-Transition Caching**: Implemented Streamlit's `@st.cache_data` decorators across computationally expensive ML functions (`generate_cohorts`, `build_pyvis_graph`, `find_nearest_teacher`). Module-switching latency has been entirely eliminated, delivering near-instantaneous navigation.
- **Geospatial Model Toggling**: Integrated dynamic UI controls (`st.radio`) directly into the Geospatial Tracker. Users can now seamlessly toggle map projections between the synthetic simulation dataset and live data piped from the AI Ingestion Engine.
- **AI Model Initialization Feedbacks**: Wrapped HuggingFace model loading (`SentenceTransformer` and `MarianMTModel`) in `@st.cache_resource` with an asynchronous visual spinner. This informs users that semantic NLP models are booting into RAM during the first load of the Ingestion Engine, hiding the loading freeze.
- **Defensive Data Forecasts**: Built exception-handling buffers around the longitudinal forecasting algorithm (`np.polyfit`) to prevent pipeline crashes when mapping array dimensions across incomplete data points.
- **Dynamic Schema Normalization**: Upgraded the core DataFrame schema dictionary to strictly maintain `PascalCase` mappings where required, successfully fixing UI parsing errors (`KeyError: 'Cohort_Name'`) and automatically deduplicating table outputs.

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
