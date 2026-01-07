import os
from faker import Faker
import random

fake = Faker()

def generate_patient_files(folder, name, mrn):
    os.makedirs(f"data/{folder}", exist_ok=True)
    for i in range(1, 11):
        file_path = f"data/{folder}/record_{i}.txt"
        with open(file_path, "w") as f:
            f.write(f"PATIENT: {name} | MRN: {mrn}\n")
            f.write(f"TYPE: {random.choice(['Lab', 'Clinic', 'Discharge'])}\n")
            f.write(f"NOTES: {fake.paragraph(nb_sentences=5)}\n")
            f.write(f"VITALS: BP {random.randint(110,140)}/80, HR {random.randint(60,100)}")

generate_patient_files("Patient_1", "Arjun Kumar", "MRN-100293")
generate_patient_files("Patient_2", "Lata Sharma", "MRN-554012")
print("✅ 20 Medical files created in data/ folder!")