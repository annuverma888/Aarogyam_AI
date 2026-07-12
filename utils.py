import pandas as pd
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

# ==========================
# Load Datasets
# ==========================

description_df = pd.read_csv(os.path.join(DATASET_DIR, "disease_description.csv"))
precaution_df = pd.read_csv(os.path.join(DATASET_DIR, "symptom_precaution.csv"))
medicine_df = pd.read_csv(os.path.join(DATASET_DIR, "medicine_dataset.csv"))
medicine_info_df = pd.read_csv(os.path.join(DATASET_DIR, "medicine_info.csv"))
diet_df = pd.read_csv(os.path.join(DATASET_DIR, "diet_dataset.csv"))
workout_df = pd.read_csv(os.path.join(DATASET_DIR, "workout_dataset.csv"))

# Remove extra spaces from column names
description_df.columns = description_df.columns.str.strip()
precaution_df.columns = precaution_df.columns.str.strip()
medicine_df.columns = medicine_df.columns.str.strip()
medicine_info_df.columns = medicine_info_df.columns.str.strip()
diet_df.columns = diet_df.columns.str.strip()
workout_df.columns = workout_df.columns.str.strip()


# ==========================
# Disease Description
# ==========================

def get_description(disease):
    row = description_df[description_df["Disease"].str.lower() == disease.lower()]
    if row.empty:
        return "No description available."
    return row.iloc[0]["Description"]


# ==========================
# Precautions
# ==========================

def get_precautions(disease):
    row = precaution_df[precaution_df["Disease"].str.lower() == disease.lower()]
    if row.empty:
        return []
    return row.iloc[0, 1:].dropna().tolist()


# ==========================
# Medicines by Disease
# ==========================

def get_medicines(disease):
    row = medicine_df[medicine_df["Disease"].str.lower() == disease.lower()]
    if row.empty:
        return []
    return row.iloc[0, 1:].dropna().tolist()


# ==========================
# Medicine Information
# ==========================

def search_medicine(medicine_name):
    result = medicine_info_df[
        medicine_info_df["Medicine"].str.contains(
            medicine_name,
            case=False,
            na=False
        )
    ]

    if result.empty:
        return None

    return result.iloc[0].to_dict()


# ==========================
# Diet
# ==========================

def get_diet(disease):
    row = diet_df[diet_df["Disease"].str.lower() == disease.lower()]
    if row.empty:
        return {}

    return {
        "Breakfast": row.iloc[0]["Breakfast"],
        "Lunch": row.iloc[0]["Lunch"],
        "Dinner": row.iloc[0]["Dinner"],
        "Avoid": row.iloc[0]["Avoid"]
    }


# ==========================
# Workout
# ==========================

def get_workout(disease):
    row = workout_df[workout_df["Disease"].str.lower() == disease.lower()]
    if row.empty:
        return {}

    return {
        "Exercise 1": row.iloc[0]["Exercise_1"],
        "Exercise 2": row.iloc[0]["Exercise_2"],
        "Exercise 3": row.iloc[0]["Exercise_3"],
        "Duration": row.iloc[0]["Duration"]
    }
    
    
def detect_symptoms(text, symptoms):

    text = text.lower()

    detected = []

    for symptom in symptoms:

        symptom_name = symptom.replace("_", " ")

        if symptom_name in text:
            detected.append(symptom)

    return detected


