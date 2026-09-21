
import streamlit as st
import pickle
import pandas as pd

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Healthcare AI",
    page_icon="🏥",
    layout="wide"
)

# =========================================================
# LOAD MODEL
# =========================================================

with open("disease_model.pkl", "rb") as file:
    model = pickle.load(file)

with open("symptom_encoder.pkl", "rb") as file:
    mlb = pickle.load(file)

with open("feature_columns.pkl", "rb") as file:
    feature_columns = pickle.load(file)

# =========================================================
# PREDICTION FUNCTION
# =========================================================

def predict_disease(age, symptoms):

    symptom_vector = pd.DataFrame(
        0,
        index=[0],
        columns=mlb.classes_
    )

    symptoms = [symptom.strip().lower() for symptom in symptoms]

    for symptom in symptoms:
        if symptom in symptom_vector.columns:
            symptom_vector.loc[0, symptom] = 1

    symptom_vector["Age"] = age
    symptom_vector["Symptom_Count"] = len(symptoms)

    symptom_vector = symptom_vector[feature_columns]

    prediction = model.predict(symptom_vector)[0]

    return prediction


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.hero {
    padding: 40px;
    border-radius: 20px;
    background: linear-gradient(135deg, #e8f5ff, #f5fbff);
    text-align: center;
    margin-bottom: 30px;
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 10px;
}

.hero p {
    font-size: 18px;
    color: #555;
}

.card {
    padding: 25px;
    border-radius: 16px;
    background: white;
    border: 1px solid #e5e7eb;
    margin-bottom: 20px;
}

.prediction {
    padding: 30px;
    border-radius: 18px;
    background: #eefbf3;
    border: 1px solid #b7e4c7;
    text-align: center;
    margin-top: 25px;
}

.prediction h2 {
    font-size: 32px;
}

.warning {
    padding: 18px;
    border-radius: 12px;
    background: #fff8e1;
    border: 1px solid #ffe082;
    margin-top: 20px;
}

.section-title {
    margin-top: 35px;
    margin-bottom: 20px;
}

.stat {
    text-align: center;
    padding: 20px;
    border-radius: 15px;
    background: #f7f9fc;
}

.stat h2 {
    margin-bottom: 5px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero">

<h1>🏥 Personalized Healthcare AI</h1>

<p>
AI-assisted health assessment and general healthcare information system
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# STATISTICS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="stat">
    <h2>25,000+</h2>
    <p>Training Records</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat">
    <h2>30</h2>
    <p>Condition Classes</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat">
    <h2>28</h2>
    <p>Symptoms</p>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# HEALTH ASSESSMENT
# =========================================================

st.markdown(
    '<h2 class="section-title">🩺 Health Assessment</h2>',
    unsafe_allow_html=True
)

st.write(
    "Enter your basic information and select the symptoms you are experiencing."
)

col1, col2 = st.columns(2)

with col1:
    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=25
    )

with col2:
    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"]
    )


# =========================================================
# SYMPTOMS
# =========================================================

st.subheader("Select Symptoms")

symptoms_list = list(mlb.classes_)

selected_symptoms = []

columns = st.columns(4)

for i, symptom in enumerate(symptoms_list):

    with columns[i % 4]:

        selected = st.checkbox(
            symptom.title(),
            key=f"symptom_{i}"
        )

        if selected:
            selected_symptoms.append(symptom)


# =========================================================
# ANALYZE BUTTON
# =========================================================

st.write("")

if st.button(
    "🔍 Analyze Symptoms",
    type="primary",
    use_container_width=True
):

    if len(selected_symptoms) == 0:

        st.warning(
            "Please select at least one symptom."
        )

    else:

        prediction = predict_disease(
            age,
            selected_symptoms
        )

        # Store result
        st.session_state["prediction"] = prediction
        st.session_state["age"] = age
        st.session_state["gender"] = gender
        st.session_state["symptoms"] = selected_symptoms

        st.success("Health assessment completed.")


# =========================================================
# RESULT
# =========================================================

if "prediction" in st.session_state:

    prediction = st.session_state["prediction"]

    st.markdown("""
    <div class="prediction">

    <p><strong>MODEL PREDICTION</strong></p>

    </div>
    """, unsafe_allow_html=True)

    st.subheader(
        f"Possible Condition: {prediction}"
    )

    st.write(
        "The result above is generated by the machine-learning model "
        "based on the information provided."
    )

    st.info(
        "This prediction is for educational and demonstration purposes "
        "only and should not be considered a medical diagnosis."
    )


# =========================================================
# GENERAL MEDICINE INFORMATION
# =========================================================

st.markdown(
    '<h2 class="section-title">💊 General Medicine Information</h2>',
    unsafe_allow_html=True
)

medicine_col1, medicine_col2, medicine_col3 = st.columns(3)

with medicine_col1:

    st.markdown("""
    <div class="card">

    <h3>🤒 Cold & Fever</h3>

    <p>
    Some commonly used over-the-counter medicines may provide
    temporary relief from fever and cold symptoms.
    </p>

    <strong>Example:</strong>
    <p>Paracetamol is commonly used for fever and pain relief.</p>

    </div>
    """, unsafe_allow_html=True)


with medicine_col2:

    st.markdown("""
    <div class="card">

    <h3>🩺 Allergy Symptoms</h3>

    <p>
    Certain antihistamine medicines may be used for some
    allergy-related symptoms.
    </p>

    <strong>Important:</strong>
    <p>
    Some medicines can cause drowsiness or interact with
    other medicines.
    </p>

    </div>
    """, unsafe_allow_html=True)


with medicine_col3:

    st.markdown("""
    <div class="card">

    <h3>🛡️ Medicine Safety</h3>

    <p>
    Medicine safety depends on age, allergies, existing
    conditions and other medicines being taken.
    </p>

    <strong>Remember:</strong>
    <p>
    Always consult a doctor or pharmacist before starting
    prescription medicines.
    </p>

    </div>
    """, unsafe_allow_html=True)


# =========================================================
# HEALTH RECOMMENDATIONS
# =========================================================

st.markdown(
    '<h2 class="section-title">❤️ Recommended Next Steps</h2>',
    unsafe_allow_html=True
)

rec1, rec2, rec3, rec4 = st.columns(4)

recommendations = [
    ("01", "Review Symptoms", "Check whether the information entered is accurate."),
    ("02", "Consult Professional", "Discuss persistent or concerning symptoms with a healthcare professional."),
    ("03", "Keep Records", "Maintain records of symptoms, medicines and allergies."),
    ("04", "Emergency Care", "Seek urgent care for severe breathing difficulty, unconsciousness or severe chest pain.")
]

for col, rec in zip(
    [rec1, rec2, rec3, rec4],
    recommendations
):

    with col:

        st.markdown(f"""
        <div class="card">

        <h2>{rec[0]}</h2>

        <h3>{rec[1]}</h3>

        <p>{rec[2]}</p>

        </div>
        """, unsafe_allow_html=True)


# =========================================================
# SYSTEM WORKFLOW
# =========================================================

st.markdown(
    '<h2 class="section-title">⚙️ System Workflow</h2>',
    unsafe_allow_html=True
)

workflow1, workflow2, workflow3, workflow4 = st.columns(4)

workflow = [
    ("01", "User Input", "Age, gender and symptoms"),
    ("02", "Data Processing", "Symptoms converted into features"),
    ("03", "ML Model", "Naive Bayes processes the features"),
    ("04", "Prediction", "Possible condition is displayed")
]

for col, step in zip(
    [workflow1, workflow2, workflow3, workflow4],
    workflow
):

    with col:

        st.markdown(f"""
        <div class="card">

        <h2>{step[0]}</h2>

        <h3>{step[1]}</h3>

        <p>{step[2]}</p>

        </div>
        """, unsafe_allow_html=True)


# =========================================================
# ABOUT
# =========================================================

st.markdown(
    '<h2 class="section-title">ℹ️ About the System</h2>',
    unsafe_allow_html=True
)

st.write("""
The Personalized Healthcare and Medicine Recommendation System
is a machine-learning based educational application.

The system accepts basic user information and symptoms,
converts the symptoms into machine-readable features and
uses a trained Naive Bayes model to generate a possible
condition prediction.

The application also provides general medicine information,
health recommendations and safety guidance.
""")


# =========================================================
# TECHNOLOGY STACK
# =========================================================

st.subheader("Technology Stack")

tech1, tech2, tech3, tech4, tech5 = st.columns(5)

with tech1:
    st.write("🐍 Python")

with tech2:
    st.write("📊 Pandas")

with tech3:
    st.write("🤖 Scikit-learn")

with tech4:
    st.write("🎨 Streamlit")

with tech5:
    st.write("🗃️ Machine Learning")




# =========================================================
# ASSESSMENT HISTORY
# =========================================================

if "history" not in st.session_state:
    st.session_state.history = []

# Save assessment when prediction is generated
if "prediction" in st.session_state:

    current_record = {
        "Age": st.session_state["age"],
        "Gender": st.session_state["gender"],
        "Symptoms": ", ".join(st.session_state["symptoms"]),
        "Prediction": st.session_state["prediction"]
    }

    # Add only if it is different from the last record
    if not st.session_state.history or \
       st.session_state.history[-1] != current_record:

        st.session_state.history.append(current_record)


# Display history
st.markdown(
    '<h2 class="section-title">📋 Assessment History</h2>',
    unsafe_allow_html=True
)

if st.session_state.history:

    history_df = pd.DataFrame(st.session_state.history)

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

    if st.button("🗑️ Clear History"):

        st.session_state.history = []

        if "prediction" in st.session_state:
            del st.session_state["prediction"]

        st.rerun()

else:

    st.info(
        "No assessment history yet. Complete an assessment to see it here."
    )



# =========================================================
# DISCLAIMER
# =========================================================

st.markdown("""
<div class="warning">

<h3>⚠️ Medical Disclaimer</h3>

<p>
This application is intended for educational and demonstration
purposes only. The machine-learning prediction should not be
considered a medical diagnosis or prescription.
</p>

<p>
Always consult a qualified healthcare professional for medical
advice, diagnosis and treatment.
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.write("")

st.markdown(
    "<center>🏥 Personalized Healthcare AI | Educational Project</center>",
    unsafe_allow_html=True
)
