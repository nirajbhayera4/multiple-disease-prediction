# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 09:45:01 2025

@author: hp
"""

import sqlite3
import datetime

def create_diagnosis_database(db_name="medical_diagnosis.db"):
    """Creates an SQLite database for medical diagnoses and a table."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patient_diagnoses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT,
                test_name TEXT,
                test_results TEXT,
                diagnosis TEXT,
                timestamp TEXT
            )
        """)

        conn.commit()
        print(f"Database '{db_name}' and table 'patient_diagnoses' created successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()

def insert_diagnosis_data(db_name="medical_diagnosis.db", data=None):
    """Inserts patient diagnosis data into the patient_diagnoses table."""
    if data is None:
        return

    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO patient_diagnoses (patient_name, test_name, test_results, diagnosis, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, data + (timestamp,))  # Append timestamp to data

        conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()

def query_diagnosis_data(db_name="medical_diagnosis.db", patient_name=None):
    """Queries and prints patient diagnosis data from the patient_diagnoses table."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        if patient_name:
            cursor.execute("SELECT * FROM patient_diagnoses WHERE patient_name = ?", (patient_name,))
        else:
            cursor.execute("SELECT * FROM patient_diagnoses")

        rows = cursor.fetchall()

        if rows:
            for row in rows:
                print(f"ID: {row[0]}, Patient: {row[1]}, Test: {row[2]}, Results: {row[3]}, Diagnosis: {row[4]}, Time: {row[5]}")
        else:
            print("No matching records found.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()

# Example usage:
create_diagnosis_database()
insert_diagnosis_data(data=("Alice Smith", "Blood Test", "Glucose: 110, Cholesterol: 200", "Prediabetes",))
insert_diagnosis_data(data=("Bob Johnson", "ECG", "Normal Sinus Rhythm", "Healthy",))
insert_diagnosis_data(data=("Niraj ", "MRI", "No abnormalities detected", "Healthy",))

print("\nAll Patient Diagnoses:")
query_diagnosis_data()

print("\nAlice Smith's Diagnoses:")
query_diagnosis_data(patient_name="Alice Smith")

print("\nNiraj's Diagnoses:")
query_diagnosis_data(patient_name="Niraj")