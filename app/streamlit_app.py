import plotly.express as px
import plotly.graph_objects as go
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import streamlit as st
import numpy as np
import pandas as pd
import joblib

from utils import (
    get_recommendation,
    get_diet_plan,
    get_exercise_plan
)
def generate_pdf(
    bmi,
    prediction_label,
    recommendation,
    diet_plan,
    exercise_plan
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    # Title
    title = Paragraph(
        "AI Obesity Health Report",
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    # BMI
    bmi_text = Paragraph(
        f"<b>BMI:</b> {bmi:.2f}",
        styles['BodyText']
    )

    elements.append(bmi_text)

    elements.append(Spacer(1, 12))

    # Prediction
    prediction_text = Paragraph(
        f"<b>Prediction:</b> {prediction_label}",
        styles['BodyText']
    )

    elements.append(prediction_text)

    elements.append(Spacer(1, 12))

    # Recommendation
    recommendation_text = Paragraph(
        f"<b>Recommendation:</b><br/>{recommendation}",
        styles['BodyText']
    )

    elements.append(recommendation_text)

    elements.append(Spacer(1, 12))

    # Diet Plan
    diet_string = "<br/>".join(diet_plan)

    diet_text = Paragraph(
        f"<b>Diet Plan:</b><br/>{diet_string}",
        styles['BodyText']
    )

    elements.append(diet_text)

    elements.append(Spacer(1, 12))

    # Exercise Plan
    exercise_string = "<br/>".join(exercise_plan)

    exercise_text = Paragraph(
        f"<b>Exercise Plan:</b><br/>{exercise_string}",
        styles['BodyText']
    )

    elements.append(exercise_text)

    # Build PDF
    doc.build(elements)

    buffer.seek(0)

    return buffer
# Load model
model = joblib.load("../models/obesity_model.pkl")
target_encoder = joblib.load("../models/target_encoder.pkl")

# Page config
st.set_page_config(
    page_title="AI Obesity Risk Predictor",
    page_icon="🏥",
    layout="wide"
)
st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

h1, h2, h3, h4 {
    color: #00FFAA;
}

.stButton>button {
    background-color: #FF4B4B;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 18px;
    border: none;
}

.stButton>button:hover {
    background-color: #FF2E2E;
    color: white;
}

.result-box {
    padding: 20px;
    border-radius: 10px;
    background-color: #14532d;
    color: red;
    font-size: 28px;
    font-weight: bold;
    text-align: center;
    border: 2px solid #22c55e;
    box-shadow: 0px 0px 15px rgba(34,197,94,0.5);
}

</style>
""", unsafe_allow_html=True)
# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 18px;
}

.stButton>button:hover {
    background-color: #ff1f1f;
}

.result-box {
    padding: 20px;
    border-radius: 10px;
    background-color: #e8f5e9;
    font-size: 22px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🏥 AI Healthcare Dashboard")

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Prediction", "Analytics", "About"]
)

# HOME PAGE
if page == "Home":

    st.title("🏥 Obesity Risk Level Classifier")

    st.image(
        "https://cdn-icons-png.flaticon.com/512/2966/2966486.png",
        width=150
    )

    st.markdown("""
    ## Welcome

    This AI-powered healthcare application predicts obesity risk levels
    based on lifestyle, eating habits, and physical activity.

    ### Features
    ✅ BMI Calculator  
    ✅ Obesity Prediction  
    ✅ Health Recommendations  
    ✅ AI-Based Analysis  
    """)

# PREDICTION PAGE
elif page == "Prediction":

    st.title("🧠 Obesity Prediction System")

    col1, col2 = st.columns(2)

    with col1:

        gender = st.selectbox("Gender", ["Male", "Female"])

        age = st.slider("Age", 10, 80, 25)

        height = st.number_input(
            "Height (meters)",
            1.0, 2.5, 1.70
        )

        weight = st.number_input(
            "Weight (kg)",
            20, 200, 70
        )

        family_history = st.selectbox(
            "Family History with Overweight?",
            ["yes", "no"]
        )

        favc = st.selectbox(
            "Frequent High Calorie Food Consumption?",
            ["yes", "no"]
        )

        fcvc = st.slider(
            "Vegetable Consumption Frequency",
            1, 5, 3
        )

        ncp = st.slider(
            "Number of Main Meals",
            1, 5, 3
        )

    with col2:

        caec = st.selectbox(
            "Food Between Meals",
            ["no", "Sometimes", "Frequently", "Always"]
        )

        smoke = st.selectbox(
            "Do you Smoke?",
            ["yes", "no"]
        )

        ch2o = st.slider(
            "Daily Water Intake",
            1, 5, 2
        )

        scc = st.selectbox(
            "Monitor Calories?",
            ["yes", "no"]
        )

        faf = st.slider(
            "Physical Activity Frequency",
            0, 5, 2
        )

        tue = st.slider(
            "Technology Usage Hours",
            0, 10, 3
        )

        calc = st.selectbox(
            "Alcohol Consumption",
            ["no", "Sometimes", "Frequently", "Always"]
        )

        mtrans = st.selectbox(
            "Transportation",
            [
                "Walking",
                "Bike",
                "Motorbike",
                "Public_Transportation",
                "Automobile"
            ]
        )

    # Encoding
    gender = 1 if gender == "Male" else 0
    family_history = 1 if family_history == "yes" else 0
    favc = 1 if favc == "yes" else 0
    smoke = 1 if smoke == "yes" else 0
    scc = 1 if scc == "yes" else 0

    caec_map = {
        "no": 0,
        "Sometimes": 1,
        "Frequently": 2,
        "Always": 3
    }

    calc_map = {
        "no": 0,
        "Sometimes": 1,
        "Frequently": 2,
        "Always": 3
    }

    mtrans_map = {
        "Walking": 0,
        "Bike": 1,
        "Motorbike": 2,
        "Public_Transportation": 3,
        "Automobile": 4
    }

    caec = caec_map[caec]
    calc = calc_map[calc]
    mtrans = mtrans_map[mtrans]

    # BMI
    bmi = weight / (height ** 2)

    st.subheader(f"📏 Calculated BMI: {bmi:.2f}")
    fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=bmi,
    title={'text': "BMI Score"},
    gauge={
        'axis': {'range': [0, 50]},
        'bar': {'color': "darkblue"},
        'steps': [
            {'range': [0, 18.5], 'color': "lightblue"},
            {'range': [18.5, 24.9], 'color': "green"},
            {'range': [25, 29.9], 'color': "yellow"},
            {'range': [30, 50], 'color': "red"},
        ],
    }
))

    st.plotly_chart(fig, use_container_width=True)

    # BMI Category
    if bmi < 18.5:
        st.info("Underweight")

    elif bmi < 25:
        st.success("Normal Weight")

    elif bmi < 30:
        st.warning("Overweight")

    else:
        st.error("Obese")

    # Prediction
    if st.button("🔍 Predict Obesity Risk"):

        features = pd.DataFrame([[
            age,
            gender,
            height,
            weight,
            calc,
            favc,
            fcvc,
            ncp,
            scc,
            smoke,
            ch2o,
            family_history,
            faf,
            tue,
            caec,
            mtrans
        ]], columns=[
            'Age',
            'Gender',
            'Height',
            'Weight',
            'CALC',
            'FAVC',
            'FCVC',
            'NCP',
            'SCC',
            'SMOKE',
            'CH2O',
            'family_history_with_overweight',
            'FAF',
            'TUE',
            'CAEC',
            'MTRANS'
        ])

        prediction = model.predict(features)
        st.write("Raw Prediction:", prediction)
        label_map = {

    0: "Underweight",

    1: "Normal",

    2: "Overweight",

    3: "Overweight High Risk",

    4: "Obesity Level 1",

    5: "Obesity Level 2",

    6: "Severe Obesity"
}
        prediction_label = label_map[int(prediction[0])]
        st.write("Decoded Prediction:", prediction_label)
        st.success(
            f"Predicted Risk Level: {prediction_label}") 
        st.markdown(
            f"""
            <div class="result-box">
            Predicted Risk Level: {prediction_label}
            </div>
            """,unsafe_allow_html=True
            )
        recommendation = get_recommendation(prediction_label)
        st.warning(recommendation)
        # Analytics Chart
        analytics_df = pd.DataFrame({
            "Category": ["Your BMI", "Healthy BMI"],
            "Value": [bmi, 24.9]
            })
        fig2 = px.bar(
            analytics_df,
            x="Category",
            y="Value",
            text="Value",
            title="BMI Analytics Comparison"
            )
        st.plotly_chart(fig2, use_container_width=True)
        # Diet Plan
        st.subheader("🍎 Recommended Diet Plan")
        diet_plan = get_diet_plan(prediction_label)
        for food in diet_plan:
            st.write(f"✅ {food}")

        # Exercise Plan
       
        st.subheader("🏃 Recommended Exercise Plan")

        exercise_plan = get_exercise_plan(prediction_label)
        for exercise in exercise_plan:
            st.write(f"🔥 {exercise}")

# Generate PDF
        pdf = generate_pdf(
            bmi,
            prediction_label,
            recommendation,
            diet_plan,
            exercise_plan
            )
        st.download_button(
            label="📥 Download Health Report",
            data=pdf,
            file_name="health_report.pdf",
            mime="application/pdf"
            )
# ANALYTICS PAGE
elif page == "Analytics":
        st.subheader("🧠 Feature Importance")
        import matplotlib.pyplot as plt
        feature_importance = model.feature_importances_
        feature_names = [
            'Age',
            'Gender',
            'Height',
            'Weight',
            'CALC',
            'FAVC',
            'FCVC',
            'NCP',
            'SCC',
            'SMOKE',
            'CH2O',
            'family_history_with_overweight',
            'FAF',
            'TUE',
            'CAEC',
            'MTRANS'
            ]
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(feature_names, feature_importance)
        ax.set_title("Feature Importance")
        ax.set_xlabel("Importance")
        st.pyplot(fig)
        st.title("📊 Health Analytics Dashboard")

    # Load dataset
        df = pd.read_csv("../data/obesity.csv")
        st.subheader("Dataset Preview")
        st.dataframe(df.head())

    # Obesity Distribution
        st.subheader("Obesity Level Distribution")
        obesity_counts = df["NObeyesdad"].value_counts()
        st.bar_chart(obesity_counts)

    # BMI Visualization
        st.subheader("BMI Distribution")
        bmi = df["Weight"] / (df["Height"] ** 2)
        bmi_df = pd.DataFrame({
            "BMI": bmi
            })
        st.line_chart(bmi_df)

    # Statistics
        st.subheader("Dataset Statistics")
        st.write(df.describe())

    # Correlation Heatmap
        st.subheader("Feature Correlation")
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        corr = numeric_df.corr()
        st.dataframe(corr)
# ABOUT PAGE
elif page == "About":
    st.title("ℹ️ About Project")

    st.markdown("""
    ## AI Obesity Risk Predictor

    This project uses Machine Learning to predict obesity
    risk levels based on:

    - Eating habits
    - Physical activity
    - Lifestyle patterns
    - Health indicators

    ### Technologies Used
    - Python
    - Scikit-learn
    - Streamlit
    - Flask
    - Pandas
    - NumPy

    ### Developed For
    Internship Machine Learning Project""")