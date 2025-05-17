# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 12:03:40 2024

@author: hp
"""
 
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import disease_database  #importing database file




# Load the models
diabetes_model = pickle.load(open('C:/Users/hp/Desktop/multiple disease prediction/ml models/diabetes_model.sav', 'rb'))
heart_model = pickle.load(open('C:/Users/hp/Desktop/multiple disease prediction/ml models/heart_model.sav', 'rb'))
 


# App Configuration
st.set_page_config(
    page_title="Multiple Disease Prediction System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

 

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        'Multiple Disease Prediction System',
        ['Home', 'Diabetes Prediction', 'Heart Disease Prediction',  'History'],
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
        - **Parkinson's Disease**

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
"Moderate Alcohol Consumption: Stick to recommended limits (one drink per day for women, two for men)."

 "4.Regular Medical Checkups",
 
"Schedule routine health checkups to monitor heart health, especially if you have a family history of heart disease.",
"Follow your doctor’s recommendations for medications or lifestyle adjustments."
    ],
    "Parkinson’s": [
        "1. Engage in Regular Physical Activity",
        
"Exercise for Balance and Coordination: Regular exercise, especially activities like walking, tai chi, or yoga, can help improve balance, flexibility, and coordination, which are essential in managing Parkinson’s disease symptoms.",
"Strength Training: Incorporating weight-bearing exercises can improve muscle strength and reduce the risk of falls.",
"Aerobic Exercise: Activities like swimming, cycling, or dancing can increase blood flow to the brain and potentially reduce the risk of neurodegenerative diseases.",

"2. Eat a Healthy and Balanced Diet",

"Antioxidant-Rich Foods: Include foods high in antioxidants, such as berries, nuts, spinach, and broccoli, to protect the brain from oxidative stress.",
"Omega-3 Fatty Acids: Eat fish like salmon and mackerel or plant-based sources like flaxseeds and chia seeds to support brain health.",

"3. Stay Mentally Active",

"Engage in Brain-Boosting Activities: Solve puzzles, read books, or engage in activities that challenge the mind and stimulate cognitive function.",
"Learn New Skills: Try new hobbies or skills like learning a musical instrument or a new language to keep your brain active.",

"4. Regular Medical Checkups",

"Consult a Neurologist: Regular checkups with a neurologist can help monitor any early symptoms and provide preventive strategies.",
"Consider Genetic Testing: If you have a family history of Parkinson’s disease, genetic counseling or testing may be helpful in assessing risk factors."
    ]
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

    # Input fields
    col1, col2, col3 = st.columns(3)
    with col1:
        Name = st.text_input('Name of the patient')
    with col2:
        Pregnancies = st.text_input('Number of Pregnancies')
    with col3:
        Glucose = st.text_input('Glucose Level')
    with col1:
        BloodPressure = st.text_input('Blood Pressure Value')
    with col2:
        SkinThickness = st.text_input('Skin Thickness Value')
    with col3:
        Insulin = st.text_input('Insulin Level')
    with col1:
        BMI = st.text_input('BMI Value')
    with col2:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function Value')
    with col3:
        Age = st.text_input('Age')

    # Code for prediction
    diab_diagnosis = ''
    st.button('Upload Report')
    str(Name)
    if st.button('Diabetes Test Result'):
        try:
            # Convert inputs to float
            diab_prediction = diabetes_model.predict([[float(Pregnancies), float(Glucose), float(BloodPressure), 
                                                       float(SkinThickness), float(Insulin), float(BMI), 
                                                       float(DiabetesPedigreeFunction), float(Age)]])
            if diab_prediction[0] == 1:
                diab_diagnosis = 'The person is Diabetic'
                st.success(diab_diagnosis)
                # Show prevention tips for diabetes
                show_prevention_tips("Diabetes")
            else:
                diab_diagnosis = 'The person is Healthy'
                st.success(diab_diagnosis)
        except ValueError:
            st.error("Please enter valid numeric inputs.")

# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':
    st.title('Heart Disease Prediction using ML')

    # Input fields
    col1, col2, col3 = st.columns(3)
    with col1:
        Name = st.text_input('Name of the patient')
    with col2:
        Age = st.text_input('Age')
    with col3:
        Sex = st.text_input('Sex (1 = Male, 0 = Female)')
    with col1:
        ChestPain = st.text_input('Chest Pain Type (0, 1, 2, or 3)')
    with col2:
        BloodPressure = st.text_input('Resting Blood Pressure')
    with col3:
        Cholesterol = st.text_input('Cholesterol Level')
    with col1:
        BloodSugar = st.text_input('Blood Sugar (1 = True, 0 = False)')
    with col2:
        ECG = st.text_input('Resting ECG (0, 1, or 2)')
    with col3:
        HeartRate = st.text_input('Max Heart Rate Achieved')
    with col1:
        InducedAngina = st.text_input('Exercise Induced Angina (1 = Yes, 0 = No)')
    with col2:
        Oldpeak = st.text_input('Oldpeak (ST Depression)')
    with col3:
        Slope = st.text_input('Slope (0, 1, or 2)')
    with col1:
        MajorVessel = st.text_input('Number of Major Vessels (0-3)')
    with col2:
        Thal = st.text_input('Thal (1 = Normal, 2 = Fixed Defect, 3 = Reversible Defect)')

    # Code for prediction
    heart_diagnosis = ''
    st.button('Upload Report')
    str(Name)
    if st.button('Heart Disease Test Result'):
        try:
            # Convert inputs to float
            heart_prediction = heart_model.predict([[float(Age), float(Sex), float(ChestPain), float(BloodPressure), 
                                                      float(Cholesterol), float(BloodSugar), float(ECG), 
                                                      float(HeartRate), float(InducedAngina), float(Oldpeak), 
                                                      float(Slope), float(MajorVessel), float(Thal)]])
            if heart_prediction[0] == 1:
                heart_diagnosis = 'The person has Heart Disease'
                st.success(heart_diagnosis)
                # Show prevention tips for heart disease
                show_prevention_tips("Heart Disease")
            else:
                heart_diagnosis = 'The person is Healthy'
                st.success(heart_diagnosis)
        except ValueError:
            st.error("Please enter valid numeric inputs.")



            
# History Page
 
if selected == 'History':
    st.title('Prediction History')

    # Load previous history from the database
    history = disease_database.query_diagnosis_data()

    # Display available history
    if history:
        for row in history:
            st.write(f"ID: {row[0]}, Patient: {row[1]}, Test: {row[2]}, Results: {row[3]}, Diagnosis: {row[4]}, Time: {row[5]}")
   

    # Input for new patient name
    new_patient_name = st.text_input("Enter a new Patient Name to add to History:")
    
    if new_patient_name:
        # Query database with the new patient name
        new_patient_history = disease_database.query_diagnosis_data(patient_name=new_patient_name)
        
        if new_patient_history:
            st.write("Newly entered patient history:")
            for row in new_patient_history:
                st.write(f"ID: {row[0]}, Patient: {row[1]}, Test: {row[2]}, Results: {row[3]}, Diagnosis: {row[4]}, Time: {row[5]}")
        else:
            st.write(f"No history available for {new_patient_name}.")
