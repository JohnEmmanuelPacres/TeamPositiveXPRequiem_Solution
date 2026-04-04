# Team PositiveXPRequiem | A.S.T.R.A Framework

**START-DOST Hackathon Solution: Decision Support System (DSS)**

This project is a professional-grade predictive Decision Support System (DSS) designed to track, analyze, and mitigate structural risks—specifically **out-of-field teaching**—in the Philippine science and mathematics education sector.

By unifying fragmented data, the **A.S.T.R.A** framework acts as a mathematical playbook for strategic resource allocation, leveraging **Prescriptive Intelligence** to heal educational vulnerabilities system-wide.

## Table of Contents

- [Hackathon Highlights & Core Features](#hackathon-highlights--core-features)
- [Architecture Overview](#architecture-overview)
  - [The Technology Stack](#the-technology-stack)
  - [The Four Core Pillars](#the-four-core-pillars)
- [Recent Updates & Optimizations](#recent-updates--optimizations)
- [Hackathon End-to-End Simulation Walkthrough](#hackathon-end-to-end-simulation-walkthrough)
  - [1. Activating the Security Gateway](#1-activating-the-security-gateway)
  - [2. The Ingestion Engine (Automated Data Fusion)](#2-the-ingestion-engine-automated-data-fusion)
  - [3. Prescriptive Intelligence Engine (Analytics)](#3-prescriptive-intelligence-engine-analytics)
  - [4. Deployment Logistics Map (Live Operations)](#4-deployment-logistics-map-live-operations)
  - [5. Individualized Teacher View (Localized UI)](#5-individualized-teacher-view-localized-ui)
- [Methodology & Mathematical Formalization](#methodology--mathematical-formalization)
  - [1. The Fragility Index](#1-the-fragility-index)
  - [2. Workforce Clustering (K-Means)](#2-workforce-clustering-k-means)
  - [3. Stochastic Degradation Model (Timeframe Simulator)](#3-stochastic-degradation-model-timeframe-simulator)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Dashboard](#running-the-dashboard)
  - [Local Native Execution](#local-native-execution)
  - [Using Docker](#using-docker)

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

To prepare for prototype presentation and ensure a seamless, production-ready user experience, several core engine and UI optimizations were recently implemented:

- **Mentorship Ecosystem Overhaul**: Upgraded the _Intelligence Hub_ with sleek UI metric cards and transitioned from standard Plotly overlays to GPU-accelerated **`go.Scattergl`**. This resolved browser lagging issues when visualizing dense cohort demographic scatter plots.
- **Micro-Transition Caching**: Implemented Streamlit's `@st.cache_data` decorators across computationally expensive ML functions (`generate_cohorts`, `build_pyvis_graph`, `find_nearest_teacher`). Module-switching latency has been entirely eliminated, delivering near-instantaneous navigation.
- **Geospatial Model Toggling**: Integrated dynamic UI controls (`st.radio`) directly into the Geospatial Tracker. Users can now seamlessly toggle map projections between the synthetic simulation dataset and live data piped from the AI Ingestion Engine.
- **AI Model Initialization Feedbacks**: Wrapped HuggingFace model loading (`SentenceTransformer` and `MarianMTModel`) in `@st.cache_resource` with an asynchronous visual spinner. This informs users that semantic NLP models are booting into RAM during the first load of the Ingestion Engine, hiding the loading freeze.
- **Defensive Data Forecasts**: Built exception-handling buffers around the longitudinal forecasting algorithm (`np.polyfit`) to prevent pipeline crashes when mapping array dimensions across incomplete data points.
- **CSV-Backed Security Gateway**: Implemented an explicit, CSV database-backed login gateway using `st.stop()` that prevents unauthorized rendering of administrative tools. Isolated accounts dynamically inject localized dashboards based on specific "Admin" vs "Teacher" allocations mapping straight to the dataset.
- **Contextual AI Override for Deployment Logistics**: Upgraded the `geospatial_tracker` to perform contextual decision intelligence. It dynamically shifts high-priority operational targets (such as "BARMM") into focus when they fall within a 2.0% mathematical margin of the absolute highest fragility threshold.
- **Lazy-Loaded ML Engines**: Strategically decoupled heavy neural-network imports (`torch`, `sentence_transformers`) from the main-level runtime. Modules now map to the PyTorch memory footprint exclusively during active execution, dropping UI module-switching latencies to zero.
- **Data Pipeline Quality Gates**: Fortified the `ingestion` module with an interactive staging buffer. Deployed three-tier checkpoints preventing the ingestion of files with `< 500` rows or missing baseline systemic requirements.

## Hackathon End-to-End Simulation Walkthrough

To demo the comprehensive capability of the A.S.T.R.A framework to the judges, follow this standard operational sequence:

### 1. Activating the Security Gateway
1. Open the application. You will be intercepted entirely by the **Secure Authentication Gateway**.
2. **Demo Admin Access:** Log in using `admin` / `dost2026`. This unlocks the high-level operational modules (Geospatial Map, Intelligence Hub).
3. **Demo Localized Teacher Access:** Showcasing `2026-STAR-0003` / `fernandez123` demonstrates how the UI natively restructures around an isolated individual displaying localized "Career Skill-Trees".

### 2. The Ingestion Engine (Automated Data Fusion)
1. As the Admin, navigate to the **Ingestion Engine**.
2. Address the problem: local operational CSVs often contain unstructured, messy Tagalog terminology. 
3. Upload `STAR_Integrated_Data_Latest.csv` and trigger **Execute AI Fusion**.
4. Demonstrate how the local Multilingual NLP dynamically aligns Tagalog variables (`guro`, `lugar`) into the strict data schema pipeline.
5. Highlight the **Data Pipeline Quality Gates**: Explain how the engine stages data in memory first, verifying volume bounds (500+) and critical structural features before allowing you to **Confirm & Integrate**.

### 3. Prescriptive Intelligence Engine (Analytics)
1. Navigate to the **Intelligence Analytics** tab. 
2. Point out the **National Fragility Average**. Explain the methodology where K-Means Machine Learning dynamically clusters the active grid into mathematical categories ("Novice Pool" vs "Core Tier").

### 4. Deployment Logistics Map (Live Operations)
1. Open the **Deployment Logistics Map**.
2. Highlight the WebGL 3D PyDeck visualization of workforce densities. Select the **Underserved Hotspots (Out-of-Field)** toggle to instantly expose out-of-field teaching discrepancies.
3. Observe the **AI Regional Suggestion** panel. Demonstrate its real-world system awareness (how the AI utilizes a "Contextual Override" flag to target strategically critical regions).
4. Utilize the Simulation UI to deploy a specialized teacher from `Global Nearest` directly into an `AI Epicenter`. 
5. Emphasize the live recalculation: Watch the UI draw dynamic transport routing arcs while the underlying Fragility Statistics recalculate themselves in real-time. Attempt an invalid extraction to demonstrate the **Cannibalization Block** safety limit!

### 5. Individualized Teacher View (Localized UI)
1. Hit **Logout** to kill the Admin session and simulate an individual employee logging into their private portal using `2026-STAR-0003` / `fernandez123`.
2. Emphasize how the global UI instantly collapses down into specific, private metrics. 
3. Navigate to **Career Skill-Tree (Analytics)**. Show the RPG-styled Plotly Radar Chart visually summarizing the logged-in teacher's exact capabilities against their regional mathematical cohort averages.
4. Switch to **Local Ecosystem (Network)**. Demonstrate the PyVis graph rendering an isolated topological web, showing exactly who the individual teacher's localized "Veteran Legends" and mentees are strictly within their immediate jurisdiction.

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
