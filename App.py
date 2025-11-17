import streamlit as st
import math

# Conversion factor
LBS_TO_KG = 0.453592

# --- DRUG LOOKUP TABLE ---
# Data structure: 
# "Drug Name": (Dose Rate in mg/kg, Concentration in mg/mL)
DRUG_DATA = {
    "Select a Medication": (0.0, 0.0),
    "Toltrazuril (Tolt)": (33.0, 50.0), # Based on 0.3ml/lb ratio and 50mg/ml concentration
    "Panacur (Fenbendazole)": (44.1, 100.0), # Based on 1ml/5lbs ratio and 100mg/ml concentration
    "Amoxicillin (Oral Sus.)": (10.0, 50.0),
    "Metronidazole (Oral Susp.)": (15.0, 50.0),
    "Dewormer (Pyrantel Pamoate)": (5.0, 50.0), 
    "Doxycycline (Oral Sus.)": (5.0, 50.0),
    "Clavamox (Amoxi/Clav)": (13.75, 62.5),
}

def calculate_volume(weight_kg, dose_rate_mg_kg, concentration_mg_ml):
    """Calculates the volume (mL) of medication needed."""
    if concentration_mg_ml <= 0 or weight_kg <= 0:
        return 0.0
    
    # Formula: Volume (mL) = (Weight (kg) * Dose Rate (mg/kg)) / Concentration (mg/mL)
    volume_ml = (weight_kg * dose_rate_mg_kg) / concentration_mg_ml
    
    # Round to two decimal places for practical dosing (e.g., 0.15 mL)
    return round(volume_ml, 2)

st.set_page_config(page_title="OPA Med Calculator", layout="centered")

# --- 1. ADD THE LOGO ---
# NOTE: The image file 'IMG_1405.jpeg' MUST be uploaded to your GitHub repository 
# alongside this 'app.py' file for the logo to appear.
st.image("IMG_1405.jpeg", width=250) 
# The width is set to 250px, which looks good on mobile. You can adjust this number.

st.title("💊 OPA Med Calculator")
st.markdown("---")

# --- Medication Selection ---
st.header("1. Select Medication")
selected_drug = st.selectbox("Choose a common drug:", list(DRUG_DATA.keys()))

# Retrieve values based on selection
if selected_drug == "Select a Medication":
    st.warning("Please select a medication to begin.")
    dose_rate = 0.0
    concentration = 0.0
else:
    dose_rate, concentration = DRUG_DATA[selected_drug]
    
    st.info(f"""
        **Drug Data Used:**
        - **Dose Rate:** {dose_rate} mg/kg
        - **Concentration:** {concentration} mg/mL
    """)

st.markdown("---")

# --- Animal Details ---
st.header("2. Animal Weight(s) in LBS")
# The unit is now fixed to 'lbs'
unit = 'lbs'

# Use a text area for easy entry of a list of weights (for litters)
weights_input = st.text_area(
    "Enter animal weights in **LBS** (one per line, e.g., for a litter):",
    "2.5\n3.1\n2.9"
)

# --- Calculation and Output ---
if st.button("Calculate Doses"):
    
    if selected_drug == "Select a Medication":
        st.error("Please select a valid medication before calculating.")
    else:
        # Clean and convert the list of weights
        raw_weights = [w.strip() for w in weights_input.split('\n') if w.strip()]
        
        if not raw_weights:
            st.warning("Please enter at least one animal weight.")
        else:
            st.header("3. Results")
            
            total_volume = 0.0 # Initialize total volume accumulator
            
            # Process each weight
            for i, weight_str in enumerate(raw_weights):
                try:
                    weight_lbs = float(weight_str)
                    
                    # Convert LBS to KG automatically
                    weight_kg = weight_lbs * LBS_TO_KG
                    
                    volume = calculate_volume(weight_kg, dose_rate, concentration)
                    
                    # Add to the total volume
                    total_volume += volume
                    
                    # Display result for each animal
                    st.success(
                        f"**Animal {i+1} ({weight_lbs} lbs):** **{volume} mL**"
                    )
                    
                except ValueError:
                    st.error(f"Error: Weight '{weight_str}' is not a valid number.")

            # Display the total volume for the entire litter
            if raw_weights:
                st.markdown("---")
                st.success(
                    f"**LITTER TOTAL (One Dose):** **{round(total_volume, 2)} mL**"
                )
