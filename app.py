import streamlit as st
import numpy as np
import pickle
import os



st.set_page_config(
    page_title="Diabetes Predicter | Abhi",
    page_icon="🩺",
    layout="centered"
)



st.title("🩺 Diabetes Prediction System")
st.caption("Machine Learning–based medical decision support system")

st.markdown("---")



@st.cache_resource
def load_model():
    model_path = "model.pkl"

    if not os.path.exists(model_path):
        st.error("❌ model.pkl not found in project folder.")
        st.stop()

    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        st.error(f"❌ Failed to load model: {e}")
        st.stop()

model = load_model()

st.success("✅ Model loaded successfully")



st.subheader("🔍 Patient Medical Details")

with st.form("diabetes_form"):
    pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=1)
    glucose = st.number_input("Glucose Level", min_value=50, max_value=300, value=120)
    bp = st.number_input("Blood Pressure", min_value=30, max_value=200, value=70)
    skin = st.number_input("Skin Thickness", min_value=5, max_value=100, value=25)
    insulin = st.number_input("Insulin Level", min_value=10, max_value=900, value=80)
    bmi = st.number_input("BMI", min_value=10.0, max_value=70.0, value=25.0)
    dpf = st.number_input(
        "Diabetes Pedigree Function",
        min_value=0.05,
        max_value=3.0,
        value=0.5
    )
    age = st.number_input("Age", min_value=10, max_value=100, value=30)

    submit = st.form_submit_button("Predict Diabetes")



if submit:
    input_data = np.array([[
        pregnancies,
        glucose,
        bp,
        skin,
        insulin,
        bmi,
        dpf,
        age
    ]])

    try:
        prediction = model.predict(input_data)[0]


        
        if hasattr(model, "predict_proba"):
            probability = model.predict_proba(input_data)[0][1]
        else:
            probability = None

        st.markdown("---")
        st.subheader("📊 Prediction Result")

        if prediction == 1:
            st.error("⚠️ High Risk of Diabetes Detected")
        else:
            st.success("✅ Low Risk of Diabetes")

        if probability is not None:
            st.metric(
                label="Diabetes Probability",
                value=f"{probability * 100:.2f}%"
            )
        else:
            st.warning("⚠️ Probability not supported by this model")

        st.caption(
            "⚠️ This system is for educational purposes only and not a medical diagnosis."
        )

    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")



st.markdown("---")
st.caption("Built using Machine Learning | Streamlit Deployment")


