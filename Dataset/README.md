# STAR Data Generator

This script generates synthetic teacher profile data to simulate the STAR Certification ecosystem. It models regional disparities, specifically highlighting "High Fragility" in areas like BARMM and Region VIII where subject-major mismatches are more frequent.

## Project Setup

### 1. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies:

```powershell
python -m venv .venv
```

### 2. Activate the Environment

Activate the environment based on your terminal:

**PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Command Prompt (CMD):**

```cmd
.\.venv\Scripts\activate
```

### 3. Install Dependencies

Install the required packages using the requirements file:

```powershell
pip install -r Dataset/requirements.txt
```

## Running the Script

Execute the generator to produce the dataset. The script will check for a `Dataset` folder and create one if it is missing.

```powershell
python Dataset/generate_star_data.py
```

## Data Logic and Archetypes

The script generates 3,500 records using the following logic:

| Feature | Logic |
| :--- | :--- |
| **High Fragility Regions** | BARMM and Region VIII (Lower experience, 70% subject mismatch rate). |
| **Established Regions** | NCR, Region VII, etc. (Higher experience, 80% subject alignment). |
| **Certification Level** | Set to Level 1 if experience is < 5 years or if a subject mismatch is detected. |
| **Fragility Indicator** | Flagged as High whenever Major_Specialization does not match Subject_Taught. |

## Output and Versioning

Files are saved in the `Dataset/Data` folder. The script uses a timestamp-based naming convention to prevent overwriting existing data.

* **Format:** `STAR_Integrated_Data_YYYYMMDD_HHMM.csv`

To exit the virtual environment, run:

```powershell
deactivate
```
