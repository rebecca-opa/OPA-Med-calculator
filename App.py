import streamlit as st
import math

# Conversion factor
LBS_TO_KG = 0.453592

# --- DRUG LOOKUP TABLE (REVISED) ---
# Data structure: 
# "Drug Name": (Dose Rate in mg/kg, Concentration/Pill Size in mg/unit)
# For liquids: Concentration is mg/mL
# For pills: Concentration represents the size of the pill available (mg/pill)
DRUG_DATA = {
    "Select a Medication": (0.0, 0.0, "mL"),
    "Toltrazuril (Tolt)": (33.0, 50.0, "mL"), 
    "Panacur (Fenbendazole)": (50, 100.0, "mL"), 
    # Doxy is now treated as a pill/tablet. 
    # 50.0 is the available pill size in mg (e.g., 50mg tablets).
    "Doxycycline (Pill)": (5.0, 50.0, "Pill"), 
}

def calculate_dose(weight_kg, dose_rate_mg_kg, concentration_mg_unit, unit_type):
    """
    Calculates the final dose (mL or Pill) of medication needed.
    """
    if concentration_mg_unit <= 0 or weight_kg <= 0 or dose_rate_mg_kg <= 0:
        return 0.0, "mL" # Return 0.0 and a default unit
    
    # 1. Calculate the total Milligrams (mg) needed for the animal
    total_mg_needed = weight_kg * dose_rate_mg_kg
    
    # 2. Calculate the final dose amount
    # Formula: Dose (unit) = Total mg needed / Concentration (mg/unit)
    final_dose = total_mg_needed / concentration_mg_unit
    
    # 3. Rounding for practical use
    if unit_type == "Pill":
        # Rounding to two decimals for pills allows for 1/4 or 1/2 pill dosing (e.g., 0.5 or 0.25)
        rounded_dose = round(final_dose, 2)
    else: # mL (liquid)
        # Keep rounding to two decimals for liquid volume
        rounded_dose = round(final_dose, 2)
        
    return rounded_dose, unit_type

st.set_page_config(page_title="OPA Med Calculator", layout="centered")

# --- APP START ---

# --- 1. ADD THE LOGO ---
st.image("IMG_1405.jpeg", width=250)
st.title("💊 OPA Med Calculator")
st.markdown("---")

# Initialize variables
dose_rate = 0.0
concentration = 0.0
unit_type = "mL" # Initialize the output unit
selected_drug = "Select a Medication"

# --- SIDEBAR FOR CUSTOM DOSE INPUT ---
with st.sidebar:
    st.header("⚙️ Advanced: Custom Dose")
    st.markdown("Use this section for drugs **not** listed.")
    
    custom_dose_rate = st.number_input(
        "Custom Dose Rate (mg/kg):", 
        min_value=0.0, 
        value=0.0, 
        step=0.1
    )
    custom_concentration = st.number_input(
        "Custom Concentration/Pill Size (mg/unit):", 
        min_value=0.0, 
        value=0.0, 
        step=0.1
    )
    custom_unit_type = st.selectbox(
        "Output Unit:",
        ("mL", "Pill"),
        index=0 # Default to mL
    )

# --- Medication Selection ---
st.header("1. Select Medication")
selected_drug = st.selectbox("Choose a common drug:", list(DRUG_DATA.keys()))

# Determine which drug data to use: Custom or Preset
use_custom = custom_dose_rate > 0 and custom_concentration > 0

if use_custom:
    st.warning(f"⚠️ Using **Custom** values from the sidebar. Output will be in **{custom_unit_type}**.")
    dose_rate = custom_dose_rate
    concentration = custom_concentration
    unit_type = custom_unit_type
    drug_name_display = "Custom Medication"
elif selected_drug == "Select a Medication":
    st.warning("Please select a medication to begin.")
    dose_rate = 0.0
    concentration = 0.0
    unit_type = "mL"
    drug_name_display = ""
else:
    # Use preset data
    dose_rate, concentration, unit_type = DRUG_DATA[selected_drug]
    drug_name_display = selected_drug
    
    st.info(f"""
        **Drug Data Used ({drug_name_display}):**
        - **Dose Rate:** {dose_rate} mg/kg
        - **Concentration/Pill Size:** {concentration} mg/{unit_type}
        - **Target Unit:** **{unit_type}**
    """)

st.markdown("---")

# --- Animal Details ---
st.header("2. Animal Weight(s) in LBS")

weights_input = st.text_area(
    "Enter animal weights in **LBS** (one per line, e.g., 2.5\n3.1\n2.9):",
    value="" 
)

# --- Calculation and Output ---
if st.button("Calculate Doses"):
    
    if not use_custom and selected_drug == "Select a Medication":
        st.error("Please select a valid medication or enter custom dose data.")
    elif dose_rate == 0.0 or concentration == 0.0:
        st.error("Dose rate and/or concentration cannot be zero.")
    else:
        raw_weights = [w.strip() for w in weights_input.split('\n') if w.strip()]
        
        if not raw_weights:
            st.warning("Please enter at least one animal weight in LBS.")
        else:
            st.header(f"3. Results for **{drug_name_display}**")
            
            total_dose = 0.0 # Initialize total dose accumulator
            
            for i, weight_str in enumerate(raw_weights):
                try:
                    weight_lbs = float(weight_str)
                    
                    # Convert LBS to KG automatically
                    weight_kg = weight_lbs * LBS_TO_KG
                    
                    # Calculate the dose amount and unit type
                    dose_amount, final_unit = calculate_dose(
                        weight_kg, dose_rate, concentration, unit_type
                    )
                    
                    # Add to the total dose
                    total_dose += dose_amount
                    
                    # Display result for each animal
                    st.success(
                        f"**Animal {i+1} ({weight_lbs} lbs):** **{dose_amount} {final_unit}**"
                    )
                    
                except ValueError:
                    st.error(f"Error: Weight '{weight_str}' is not a valid number.")

            # Display the total dose for the entire litter
            if raw_weights:
                st.markdown("---")
                st.balloons()
                # Use the 'unit_type' determined earlier for the final label
                st.success(
                    f"**LITTER TOTAL (One Dose):** **{round(total_dose, 2)} {unit_type}**"
                )
