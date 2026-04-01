# Team PositiveXPRequiem - DSS Platform (DOST Hackathon)

This project is a professional-grade Decision Support System (DSS) designed to track structural risks in the Philippine science and math teaching force. It aims to unify fragmented teacher data and provide a mathematical playbook for strategic resource computing, otherwise known as **Prescriptive Intelligence**.

## Architecture Overview

The system operates as a Modular Monolith in Python, running fully local to simulate high-end prescriptive analytics while guaranteeing performance on low-end hardware.

The platform is divided into Four Core Pillars:
1. **Pillar 1: Geospatial Tracker**: Project NOAH-style 3D Logistics map powered by `pydeck`.
2. **Pillar 2: Ingestion Engine**: String normalization ('Schema Healer') utility mapped using `thefuzz[speedup]` to sanitize incoming datasets natively before routing to analytic engines.
3. **Pillar 3: Network Dashboard**: Interactive node topology displaying systemic connectivity via `NetworkX` and `pyvis`.
4. **Pillar 4: Intelligence Hub**: Real-time risk math algorithms calculating local Fragility Scores and leveraging `scikit-learn` K-Means clustering to predict structural risks.

## Prerequisites

- **Python**: version 3.8+ recommended.

## Installation

We highly recommend running this solution inside a Python virtual environment to avoid native library conflicts (if you opt to use docker instead of virtual environment, scroll down to 'Using Docker' section).

1. **Create and Activate a Virtual Environment:**

   *Windows:*
   ```bash
   python -m venv venv
   .\venv\Scripts\activate

   or

   source venv/Scripts/activate
   ```
   *macOS / Linux:*
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
