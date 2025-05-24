import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# --- MongoDB Connection ---
# Use st.secrets for secure credential management in Streamlit Cloud.
# For local development, you can directly put your URI here,
# or create a .streamlit/secrets.toml file if you plan to deploy.

@st.cache_resource
def get_mongo_client():
    
    """Establishes and caches the MongoDB client connection."""
    try:
        client = MongoClient(st.secrets["mongo"]["uri"])
        # Optional: Confirm connection with a ping
        client.admin.command("ping")
        return client
    except Exception as e:
        st.error(f"Error connecting to MongoDB: {e}")
        st.stop()


@st.cache_resource
def get_database():
    """Returns the database object, creating it if it doesn't exist."""
    client = get_mongo_client()
    # Replace 'disease_prediction_db' with your desired database name
    return client.get_database("disease_prediction_db")

def get_diagnoses_collection():
    """Returns the 'diagnoses' collection."""
    db = get_database()
    return db.get_collection("diagnoses")

def insert_diagnosis_data(data):
    """
    Inserts a new diagnosis record into the MongoDB 'diagnoses' collection.

    Args:
        data (dict): A dictionary containing the diagnosis details.
                     Expected keys: 'patient_name', 'test_type', 'test_details', 'diagnosis_result'.
    """
    collection = get_diagnoses_collection()
    record = {
        "patient_name": data['patient_name'],
        "test_type": data['test_type'],
        "test_details": data['test_details'],
        "diagnosis_result": data['diagnosis_result'],
        "timestamp": datetime.now() # Store timestamp for when the record was created
    }
    try:
        collection.insert_one(record)
        return True
    except Exception as e:
        st.error(f"Error inserting diagnosis data: {e}")
        return False

@st.cache_data(ttl=60) # Cache the query results for 60 seconds
def query_diagnosis_data(patient_name=None):
    """
    Queries diagnosis history from the MongoDB 'diagnoses' collection.

    Args:
        patient_name (str, optional): If provided, filters results by patient name.

    Returns:
        list: A list of dictionaries, where each dictionary is a diagnosis record.
    """
    collection = get_diagnoses_collection()
    query = {}
    if patient_name:
        query["patient_name"] = {"$regex": patient_name, "$options": "i"} # Case-insensitive search

    try:
        # Sort by timestamp in descending order (most recent first)
        results = list(collection.find(query).sort("timestamp", -1))
        return results
    except Exception as e:
        st.error(f"Error querying diagnosis data: {e}")
        return []

# No need for create_diagnosis_database() as MongoDB creates db/collections on first insert.
# You can add index creation here if needed for performance.
# def create_indexes():
#     collection = get_diagnoses_collection()
#     collection.create_index([("patient_name", 1)])
#     collection.create_index([("timestamp", -1)])