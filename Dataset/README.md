# STAR Data Generator

This script generates synthetic teacher profile data to simulate the **STAR Certification** ecosystem. It is designed to model regional disparities, specifically highlighting "High Fragility" in areas like BARMM and Region VIII where subject-major mismatches are more frequent.

---

## Quick Start

### 1. Initialize Virtual Environment

To keep your dependencies isolated, activate the provided virtual environment:

**For PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**For Command Prompt (CMD):**

```cmd
.\.venv\Scripts\activate
```

### 2. Install Requirements

Ensure `pandas` and `numpy` are installed within your active environment:

```powershell
pip install pandas numpy
```

### 3. Run the Generator

Execute the script to produce the synthetic dataset:

```powershell
python Dataset/generate_star_data.py
```

---

## Data Logic & Archetypes

The script generates **3,500 records** using specific logic to simulate real-world educational challenges:

| Feature | Logic |
| :--- | :--- |
| **High Fragility Regions** | BARMM and Region VIII (Lower experience, 70% subject mismatch rate). |
| **Established Regions** | NCR, Region VII, etc. (Higher experience, 80% subject alignment). |
| **Certification Level** | Automatically set to **Level 1** if experience is < 5 years or if a subject mismatch is detected. |
| **Fragility Indicator** | Flagged as **High** whenever `Major_Specialization` does not match `Subject_Taught`. |

---

## Output

Files are saved in the `Dataset/` folder with a unique timestamp to prevent overwriting:

* **Format:** `STAR_Integrated_Data_YYYYMMDD_HHMM.csv`
* **Schema-Healer Ready:** The data is generated to test the robust integration of educational metadata.

---

## Maintenance

To exit the environment after your work is done, simply run:

```powershell
deactivate
```
