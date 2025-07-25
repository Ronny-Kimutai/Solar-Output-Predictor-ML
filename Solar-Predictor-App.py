import streamlit as st
import pandas as pd
import numpy as np
import joblib  # or pickle, depending on how you saved the model

# Load the trained model
model = joblib.load("solar_model.pkl")

# Streamlit app title and description
st.title("🔆 Solar Power Predictor")
st.write("Enter forecasted values below to predict DC Power output")

# Input fields
ambient = st.slider("Ambient Temperature (°C)", 10, 50, 25)
irradiation = st.slider("Irradiance (W/m²)", 0, 1200, 500)
Hour = st.slider("Hour of Day (From 6AM to 6PM)", 6, 18, 12)

# Convert W/m² to kW/m² (because model was trained in kW/m²)
irradiation_kW = irradiation / 1000  

# Derived inputs
module_temp = ambient + 15 # Assuming module temperature is ambient + 15°C
roll_avg_irr = irradiation_kW # Assuming roll average of irradiation is the same as current irradiation
roll_avg_power = 93613, # Average of dc power rolling average from the training data

# Prediction
input_df = pd.DataFrame({
    "AMBIENT_TEMPERATURE": [ambient],
    "MODULE_TEMPERATURE": 24,
    "IRRADIATION": [irradiation_kW],
    "dc_power_roll_avg": roll_avg_power,
    "irradiation_roll_avg": [roll_avg_irr],
    "Hour": [Hour]
})

# Displaying the Prediction
if st.button("Predict"):
    prediction = model.predict(input_df)[0] # Predicting DC power in watts
    prediction_kw = prediction / 1000  # Convert to kilowatts
    st.success(f"⚡ Predicted DC Power Output: {prediction_kw:.2f} kW")