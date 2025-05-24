import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import disease_database_mongo as db_mongo # Import your new MongoDB database file
import pandas as pd # Import pandas for CSV handling



from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://nirajbhayera4:<db_password>@patientsdata.iffo2he.mongodb.net/?retryWrites=true&w=majority&appName=patientsdata"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
# Ensure your MongoDB URI is configured in Streamlit secrets for deployment.
# For local testing, you can place a .streamlit/secrets.toml file in your project root:
# [mongo]
# uri = "mongodb://localhost:27017/"
# Or for Atlas:
# uri = "mongodb+srv://your_username:your_password@cluster0.abcde.mongodb.net/?retryWrites=true&w=majority"
# Make sure to replace your_username and your_password with actual credentials.

# Load the models
try:
    diabetes_model = pickle.load(open('C:/Users/hp/Desktop/multiple disease prediction/ml models/diabetes_model.sav', 'rb'))
    heart_model = pickle.load(open('C:/Users/hp/Desktop/multiple disease prediction/ml models/heart_model.sav', 'rb'))
except FileNotFoundError:
    st.error("Error: ML models not found. Please ensure 'diabetes_model.sav' and 'heart_model.sav' are in 'C:/Users/hp/Desktop/multiple disease prediction/ml models/'.")
    st.stop() # Stop the app if models can't be loaded

# App Configuration
st.set_page_config(
    page_title="Multiple Disease Prediction System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- MongoDB connection check (optional, but good for early feedback) ---
# This will try to connect when the app first starts.
# The `get_mongo_client` function in disease_database_mongo.py already handles error stopping.
db_mongo.get_mongo_client()


# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        'Multiple Disease Prediction System',
        ['Home', 'Diabetes Prediction', 'Heart Disease Prediction', 'History'],
        icons=['house','activity', 'heart-pulse', 'person-arms-up', 'book'],
        default_index=0
    )

# Home page content
if selected == 'Home':
    # Running "Welcome" Text with Red Color
    st.markdown("""
        <style>
        @keyframes runningText {
            0% {right: -100%;}
            100% {right: 100%;}
        }
        .running-text {
            position: absolute;
            white-space: nowrap;
            font-size: 50px;  /* Increased font size */
            color: red;
            font-weight: bold;
            animation: runningText 20s linear infinite;
        }
        </style>
        <div class="running-text">Welcome to the Disease Prediction System 🩺</div>
        """, unsafe_allow_html=True)

    # Title and Heading
    st.title("Multiple Disease Prediction System 🩺")

    # Introduction in a brief and minimalistic format
    st.markdown(
        """
        ### Welcome to the Health Prediction System

        This system helps you predict the risk of common diseases based on your health data.

        - **Diabetes**
        - **Heart Disease**


        Simply provide your health details, and get accurate predictions along with preventive tips.

        ### Ready to get started?
        Click on one of the disease predictions from the sidebar to begin.
        """
    )

    # Call to Action Button (Start prediction)
    st.markdown("<br>", unsafe_allow_html=True)  # Adds space
    if st.button("Start Prediction"):
        st.write("Go to the sidebar to begin predicting your health condition.")

    # Optional Section: Motivational/Engagement Message
    st.markdown("### Stay proactive about your health. Let’s get started!")


# Prevention tips dictionary
prevention_tips = {
    "Diabetes": [
        "Dietary Tips",
        "Focus on Low-Glycemic Foods:",
        "Include foods that don't spike blood sugar levels, such as beans, lentils, whole grains, and non-starchy vegetables.",
        "Use smaller plates and measure portions to avoid overeating.",
        "Increase intake of soluble fiber found in oats, nuts, seeds, and fruits like apples and berries.",
        "Avoid white bread, pastries, and other refined carbs that can cause blood sugar spikes.",
        "Consume healthy fats from sources like avocados, nuts, seeds, and olive oil instead of trans fats or saturated fats.",
        "Lifestyle Tips",
        "Combine aerobic exercises (walking, jogging, swimming) with resistance training (weights, bodyweight exercises) for maximum benefits.",
        "Drink plenty of water and avoid sugary drinks like soda and fruit juices.",
        "Aim for 7-9 hours of sleep per night to regulate hormones that affect blood sugar levels.",
        "Monitoring and Medical Care",
        "Visit your doctor regularly to monitor blood sugar levels and assess overall health.",
        "If your doctor prescribes medications, take them as directed without skipping doses.",
        "Other Tips",
        "Quit Smoking: Smoking increases the risk of type 2 diabetes and other complications.",
        "Avoid Alcohol or Drink Moderately: Excessive alcohol consumption can lead to fluctuating blood sugar levels.",
        "Stay Active Throughout the Day: Avoid sitting for long periods; take short walks or stretch every hour.",
    ],
    "Heart Disease": [
        "1. Maintain a Heart-Healthy Diet",
        "Eat More Fruits and Vegetables: Aim for at least five servings daily.",
        "Include Whole Grains: Choose whole grain bread, oats, and brown rice.",
        "Consume Healthy Fats: Use sources like avocados, nuts, seeds, and olive oil instead of saturated and trans fats.",
        "Limit Sodium Intake: Reduce processed foods and avoid adding extra salt to meals.",
        "Include Omega-3 Fatty Acids: Eat fish like salmon and mackerel or plant-based sources like flaxseeds and walnuts.",
        "2. Stay Physically Active",
        "Exercise Regularly: Engage in 30 minutes of moderate activity (e.g., walking, swimming, or cycling) at least 5 days a week.",
        "Incorporate Strength Training: Add weight-bearing exercises twice a week.",
        "Stay Active Throughout the Day: Take breaks from prolonged sitting by walking or stretching.",
        "3. Avoid Tobacco and Alcohol",
        "Quit Smoking: Smoking significantly increases the risk of heart disease. Seek support groups or cessation programs if needed.",
        "Moderate Alcohol Consumption: Stick to recommended limits (one drink per day for women, two for men).",
        "4. Regular Medical Checkups",
        "Schedule routine health checkups to monitor heart health, especially if you have a family history of heart disease.",
        "Follow your doctor’s recommendations for medications or lifestyle adjustments."
    ],
    # Removed Parkinson's tips as it's not a prediction model in this code
}

# Function to display prevention tips
def show_prevention_tips(disease):
    st.subheader(f"Prevention Tips for {disease}")
    tips = prevention_tips.get(disease, [])
    if tips:
        for tip in tips:
            st.markdown(f"- {tip}")
        # Add a download button for the tips
        tips_str = "\n".join(tips)
        st.download_button(
            label="Download Prevention Tips",
            data=tips_str,
            file_name=f"{disease}_prevention_tips.txt",
            mime="text/plain"
        )
    else:
        st.write("No prevention tips available.")

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    st.title('Diabetes Prediction using ML')

    st.markdown("### Enter Patient Details Manually:")
    # Input fields for manual entry
    col1, col2, col3 = st.columns(3)
    with col1:
        Name = st.text_input('Patient Name', key='diabetes_name_manual')
    with col2:
        Pregnancies = st.text_input('Number of Pregnancies', key='pregnancies_manual')
    with col3:
        Glucose = st.text_input('Glucose Level', key='glucose_manual')
    with col1:
        BloodPressure = st.text_input('Blood Pressure Value', key='bp_manual')
    with col2:
        SkinThickness = st.text_input('Skin Thickness Value', key='skin_manual')
    with col3:
        Insulin = st.text_input('Insulin Level', key='insulin_manual')
    with col1:
        BMI = st.text_input('BMI Value', key='bmi_manual')
    with col2:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function Value', key='dpf_manual')
    with col3:
        Age = st.text_input('Age', key='age_manual')

    # Code for manual prediction
    if st.button('Predict Diabetes (Manual Entry)'):
        if not Name:
            st.error("Please enter the patient's name to proceed with manual prediction.")
        else:
            try:
                # Convert inputs to float
                diab_prediction = diabetes_model.predict([[float(Pregnancies), float(Glucose), float(BloodPressure),
                                                           float(SkinThickness), float(Insulin), float(BMI),
                                                           float(DiabetesPedigreeFunction), float(Age)]])
                diab_diagnosis = 'The person is Diabetic' if diab_prediction[0] == 1 else 'The person is Healthy'
                st.success(diab_diagnosis)
                show_prevention_tips("Diabetes")

                # Save to database
                test_results_str = f"Preg: {Pregnancies}, Glu: {Glucose}, BP: {BloodPressure}, Skin: {SkinThickness}, Ins: {Insulin}, BMI: {BMI}, DPF: {DiabetesPedigreeFunction}, Age: {Age}"
                db_mongo.insert_diagnosis_data(
                    data={
                        "patient_name": Name,
                        "test_type": "Diabetes Test",
                        "test_details": test_results_str,
                        "diagnosis_result": diab_diagnosis
                    }
                )
                st.info("Diagnosis saved to history.")

            except ValueError:
                st.error("Please enter valid numeric inputs for all manual fields.")

    st.markdown("---")
    st.markdown("### Upload Diabetes Patient Data (CSV):")
    uploaded_file_diabetes = st.file_uploader("Choose a CSV file for Diabetes Prediction", type="csv")

    if uploaded_file_diabetes is not None:
        try:
            df = pd.read_csv(uploaded_file_diabetes)
            st.write("Uploaded Data Preview:")
            st.dataframe(df)

            required_cols_diabetes = ['Name', 'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
            if not all(col in df.columns for col in required_cols_diabetes):
                st.error(f"Missing required columns in CSV. Please ensure your CSV has: {', '.join(required_cols_diabetes)}")
            else:
                st.markdown("---")
                st.subheader("Processing Uploaded Data:")
                results_df = pd.DataFrame(columns=['Patient Name', 'Diagnosis', 'Details'])
                processed_count = 0
                for index, row in df.iterrows():
                    patient_name = row['Name']
                    try:
                        # Prepare data for prediction
                        input_data = [
                            float(row['Pregnancies']),
                            float(row['Glucose']),
                            float(row['BloodPressure']),
                            float(row['SkinThickness']),
                            float(row['Insulin']),
                            float(row['BMI']),
                            float(row['DiabetesPedigreeFunction']),
                            float(row['Age'])
                        ]
                        diab_prediction = diabetes_model.predict([input_data])
                        diab_diagnosis = 'The person is Diabetic' if diab_prediction[0] == 1 else 'The person is Healthy'

                        test_results_str = f"Preg: {row['Pregnancies']}, Glu: {row['Glucose']}, BP: {row['BloodPressure']}, Skin: {row['SkinThickness']}, Ins: {row['Insulin']}, BMI: {row['BMI']}, DPF: {row['DiabetesPedigreeFunction']}, Age: {row['Age']}"

                        # Save to database
                        db_mongo.insert_diagnosis_data(
                            data={
                                "patient_name": patient_name,
                                "test_type": "Diabetes Test (CSV)",
                                "test_details": test_results_str,
                                "diagnosis_result": diab_diagnosis
                            }
                        )
                        results_df.loc[processed_count] = [patient_name, diab_diagnosis, test_results_str]
                        processed_count += 1
                        st.write(f"✅ Processed **{patient_name}**: {diab_diagnosis}")

                    except ValueError as e:
                        st.warning(f"Skipping row for {patient_name} due to invalid numeric input: {e}")
                    except KeyError as e:
                        st.warning(f"Skipping row for {patient_name} due to missing column: {e}")

                st.markdown("---")
                st.success(f"Successfully processed {processed_count} records from the uploaded file.")
                st.dataframe(results_df) # Display summary of processed results
                st.info("All processed diagnoses from the uploaded file have been saved to history.")

        except Exception as e:
            st.error(f"Error processing uploaded file: {e}")


# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':
    st.title('Heart Disease Prediction using ML')

    st.markdown("### Enter Patient Details Manually:")
    # Input fields for manual entry
    col1, col2, col3 = st.columns(3)
    with col1:
        Name = st.text_input('Patient Name', key='heart_name_manual')
    with col2:
        Age = st.text_input('Age', key='heart_age_manual')
    with col3:
        Sex = st.text_input('Sex (1 = Male, 0 = Female)', key='heart_sex_manual')
    with col1:
        ChestPain = st.text_input('Chest Pain Type (0, 1, 2, or 3)', key='chestpain_manual')
    with col2:
        BloodPressure = st.text_input('Resting Blood Pressure', key='heart_bp_manual')
    with col3:
        Cholesterol = st.text_input('Cholesterol Level', key='cholesterol_manual')
    with col1:
        BloodSugar = st.text_input('Blood Sugar (1 = True, 0 = False)', key='bloodsugar_manual')
    with col2:
        ECG = st.text_input('Resting ECG (0, 1, or 2)', key='ecg_manual')
    with col3:
        HeartRate = st.text_input('Max Heart Rate Achieved', key='heartrate_manual')
    with col1:
        InducedAngina = st.text_input('Exercise Induced Angina (1 = Yes, 0 = No)', key='angina_manual')
    with col2:
        Oldpeak = st.text_input('Oldpeak (ST Depression)', key='oldpeak_manual')
    with col3:
        Slope = st.text_input('Slope (0, 1, or 2)', key='slope_manual')
    with col1:
        MajorVessel = st.text_input('Number of Major Vessels (0-3)', key='majorvessel_manual')
    with col2:
        Thal = st.text_input('Thal (1 = Normal, 2 = Fixed Defect, 3 = Reversible Defect)', key='thal_manual')

    # Code for manual prediction
    if st.button('Predict Heart Disease (Manual Entry)'):
        if not Name:
            st.error("Please enter the patient's name to proceed with manual prediction.")
        else:
            try:
                # Convert inputs to float
                heart_prediction = heart_model.predict([[float(Age), float(Sex), float(ChestPain), float(BloodPressure),
                                                         float(Cholesterol), float(BloodSugar), float(ECG),
                                                         float(HeartRate), float(InducedAngina), float(Oldpeak),
                                                         float(Slope), float(MajorVessel), float(Thal)]])
                heart_diagnosis = 'The person has Heart Disease' if heart_prediction[0] == 1 else 'The person is Healthy'
                st.success(heart_diagnosis)
                show_prevention_tips("Heart Disease")

                # Save to database
                test_results_str = f"Age: {Age}, Sex: {Sex}, CP: {ChestPain}, BP: {BloodPressure}, Chol: {Cholesterol}, BS: {BloodSugar}, ECG: {ECG}, HR: {HeartRate}, EA: {InducedAngina}, OP: {Oldpeak}, Slope: {Slope}, MV: {MajorVessel}, Thal: {Thal}"
                db_mongo.insert_diagnosis_data(
                    data={
                        "patient_name": Name,
                        "test_type": "Heart Disease Test",
                        "test_details": test_results_str,
                        "diagnosis_result": heart_diagnosis
                    }
                )
                st.info("Diagnosis saved to history.")

            except ValueError:
                st.error("Please enter valid numeric inputs for all manual fields.")

    st.markdown("---")
    st.markdown("### Upload Heart Disease Patient Data (CSV):")
    uploaded_file_heart = st.file_uploader("Choose a CSV file for Heart Disease Prediction", type="csv")

    if uploaded_file_heart is not None:
        try:
            df = pd.read_csv(uploaded_file_heart)
            st.write("Uploaded Data Preview:")
            st.dataframe(df)

            required_cols_heart = ['Name', 'Age', 'Sex', 'ChestPain', 'BloodPressure', 'Cholesterol', 'BloodSugar', 'ECG', 'HeartRate', 'InducedAngina', 'Oldpeak', 'Slope', 'MajorVessel', 'Thal']
            if not all(col in df.columns for col in required_cols_heart):
                st.error(f"Missing required columns in CSV. Please ensure your CSV has: {', '.join(required_cols_heart)}")
            else:
                st.markdown("---")
                st.subheader("Processing Uploaded Data:")
                results_df = pd.DataFrame(columns=['Patient Name', 'Diagnosis', 'Details'])
                processed_count = 0
                for index, row in df.iterrows():
                    patient_name = row['Name']
                    try:
                        # Prepare data for prediction
                        input_data = [
                            float(row['Age']),
                            float(row['Sex']),
                            float(row['ChestPain']),
                            float(row['BloodPressure']),
                            float(row['Cholesterol']),
                            float(row['BloodSugar']),
                            float(row['ECG']),
                            float(row['HeartRate']),
                            float(row['InducedAngina']),
                            float(row['Oldpeak']),
                            float(row['Slope']),
                            float(row['MajorVessel']),
                            float(row['Thal'])
                        ]
                        heart_prediction = heart_model.predict([input_data])
                        heart_diagnosis = 'The person has Heart Disease' if heart_prediction[0] == 1 else 'The person is Healthy'

                        test_results_str = f"Age: {row['Age']}, Sex: {row['Sex']}, CP: {row['ChestPain']}, BP: {row['BloodPressure']}, Chol: {row['Cholesterol']}, BS: {row['BloodSugar']}, ECG: {row['ECG']}, HR: {row['HeartRate']}, EA: {row['InducedAngina']}, OP: {row['Oldpeak']}, Slope: {row['Slope']}, MV: {row['MajorVessel']}, Thal: {row['Thal']}"

                        # Save to database
                        db_mongo.insert_diagnosis_data(
                            data={
                                "patient_name": patient_name,
                                "test_type": "Heart Disease Test (CSV)",
                                "test_details": test_results_str,
                                "diagnosis_result": heart_diagnosis
                            }
                        )
                        results_df.loc[processed_count] = [patient_name, heart_diagnosis, test_results_str]
                        processed_count += 1
                        st.write(f"✅ Processed **{patient_name}**: {heart_diagnosis}")

                    except ValueError as e:
                        st.warning(f"Skipping row for {patient_name} due to invalid numeric input: {e}")
                    except KeyError as e:
                        st.warning(f"Skipping row for {patient_name} due to missing column: {e}")

                st.markdown("---")
                st.success(f"Successfully processed {processed_count} records from the uploaded file.")
                st.dataframe(results_df) # Display summary of processed results
                st.info("All processed diagnoses from the uploaded file have been saved to history.")

        except Exception as e:
            st.error(f"Error processing uploaded file: {e}")

# History Page
if selected == 'History':
    st.title('Prediction History')

    # Input for filtering history by patient name
    filter_patient_name = st.text_input("Filter by Patient Name (leave blank to show all):")

    st.markdown("---") # Separator for clarity

    # Load and display history
    if filter_patient_name:
        history = db_mongo.query_diagnosis_data(patient_name=filter_patient_name)
        if not history:
            st.write(f"No history available for '{filter_patient_name}'.")
    else:
        history = db_mongo.query_diagnosis_data()
        if not history:
            st.write("No history available yet. Perform a prediction to see records here.")

    if history:
        st.subheader("Records:")
        for record in history:
            # MongoDB's _id is an ObjectId, convert to string for display if needed
            record_id = str(record.get('_id'))
            patient_name = record.get('patient_name', 'N/A')
            test_type = record.get('test_type', 'N/A')
            diagnosis_result = record.get('diagnosis_result', 'N/A')
            timestamp = record.get('timestamp', 'N/A')
            test_details = record.get('test_details', 'No details available')

            st.write(f"**Patient:** {patient_name} | **Test:** {test_type} | **Diagnosis:** {diagnosis_result} | **Time:** {timestamp.strftime('%Y-%m-%d %H:%M:%S') if isinstance(timestamp, datetime) else str(timestamp)}")
            with st.expander(f"Show details for {patient_name} - {test_type}"):
                st.write(f"**Record ID:** {record_id}")
                st.write(f"**Test Results:** {test_details}")
            st.markdown("---") # Visual separator between records