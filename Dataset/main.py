import pandas as pd
import numpy as np
import random
import os
from datetime import datetime

def generate_star_data(num_rows=3000):
    regions = ['NCR', 'Region I', 'Region III', 'Region IV-A', 'Region VII', 'Region VIII', 'BARMM']
    majors = ['Mathematics', 'Biology', 'Chemistry', 'Physics', 'General Science']
    degrees = ['Bachelor of Secondary Education', 'BS Science', 'Master of Arts in Ed', 'PhD STEM']
    
    data = []

    for i in range(num_rows):
        # Choose Region with bias
        region = random.choice(regions)
        
        # Archetype Logic: BARMM and Region VIII are "High Fragility"
        is_fragile_region = region in ['BARMM', 'Region VIII']
        
        if is_fragile_region:
            # Low experience, high mismatch probability
            age = np.random.randint(22, 45)
            years_exp = np.random.randint(1, 12)
            major = random.choice(majors)
            # 70% chance of teaching outside their major
            subject_taught = random.choice(majors) if random.random() < 0.7 else major
        else:
            # Established regions: Higher experience, better alignment
            age = np.random.randint(25, 60)
            years_exp = np.random.randint(5, 35)
            major = random.choice(majors)
            # 20% chance of mismatch
            subject_taught = major if random.random() < 0.8 else random.choice(majors)

        # Logic for STAR Certification
        cert_level = "Level 1" if years_exp < 5 or major != subject_taught else random.choice(["Level 2", "Level 3"])

        data.append({
            "Teacher_ID": f"2026-STAR-{i:04d}",
            "Region": region,
            "Age": age,
            "Years_Experience": years_exp,
            "Educational_Attainment": random.choice(degrees),
            "Major_Specialization": major,
            "Subject_Taught": subject_taught,
            "Certification_Level": cert_level,
            "Fragility_Indicator": "High" if major != subject_taught else "Low"
        })

    df = pd.DataFrame(data)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"STAR_Integrated_Data_{timestamp}.csv"
    output_folder = "Dataset"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    file_path = os.path.join(output_folder, filename)

    # Intentionally corrupt 5% of headers/data to test the "AI Schema-Healer"
    df.to_csv(file_path, index=False)
    print(f"Generated {num_rows} rows. BARMM/Reg VIII biased for fragility.")

generate_star_data(3500)