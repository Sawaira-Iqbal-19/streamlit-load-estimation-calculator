import streamlit as st
import pandas as pd

# Define the power ratings of common appliances in kW
appliance_power = {
    "Bulb": 0.06,
    "Fan": 0.075,
    "AC": 2.0,
    "Oven": 1.5,
    "Motor": 1.0,
    "Iron": 1.0,
    "Laptop Charger": 0.05,
    "Juicer": 0.3,
    "Mobile Charger": 0.01,
    "LCD/TV": 0.1,
    "Electric Bike Charger": 0.8,
    "Fridge": 0.15,
    "Washing Machine": 1.0,
    "Spinner": 0.5,
    "Geyser": 3.0
}

appliance_descriptions = {
    "Bulb": "Standard bulb for lighting.",
    "Fan": "Ceiling fan for cooling.",
    "AC": "Air conditioner for cooling or heating.",
    "Oven": "Electric oven for cooking.",
    "Motor": "Electric motor (e.g., pump).",
    "Iron": "Electric iron for clothes.",
    "Laptop Charger": "Laptop charging adapter.",
    "Juicer": "Electric juicer for fruit or vegetable extraction.",
    "Mobile Charger": "Mobile phone charger.",
    "LCD/TV": "LED/LCD TV or monitor.",
    "Electric Bike Charger": "Charger for electric two-wheelers.",
    "Fridge": "Refrigerator for food storage.",
    "Washing Machine": "Washing machine for laundry.",
    "Spinner": "Dryer spinner for clothes.",
    "Geyser": "Electric geyser for hot water."
}

# Cable size suggestion based on amperes
def suggest_cable_size(load_amperes):
    if load_amperes <= 10:
        return "1.5 mm² Cable"
    elif load_amperes <= 20:
        return "2.5 mm² Cable"
    elif load_amperes <= 30:
        return "4 mm² Cable"
    else:
        return "6 mm² Cable"

# Circuit breaker type and size suggestion
def suggest_circuit_breaker(load_amperes):
    if load_amperes <= 10:
        return "10A MCB (Miniature Circuit Breaker)"
    elif load_amperes <= 20:
        return "20A MCB"
    elif load_amperes <= 30:
        return "30A ELCB (Earth Leakage Circuit Breaker)"
    else:
        return "40A RCCB (Residual Current Circuit Breaker)"

# Convert load from kW to Amperes (assuming 230V)
def kw_to_amperes(kw):
    voltage = 230
    return kw * 1000 / voltage

# Calculate energy cost in PKR
def calculate_energy_cost(total_kw, hours_per_day=4, cost_per_kwh=7):
    daily_kwh = total_kw * hours_per_day
    monthly_kwh = daily_kwh * 30
    return monthly_kwh * cost_per_kwh

# Total load calculation
def calculate_total_load(appliances):
    return sum(appliance_power[app] * qty for app, qty in appliances.items())

# UI Start
st.set_page_config(page_title="Home Load Estimation", layout="centered")
st.title("🏡 Home Load Estimation Tool")

# Energy cost input
unit_cost = st.number_input("Enter Cost per Unit (₨/kWh)", min_value=1.0, value=7.0)

# Room template option
room_templates = {
    "Bedroom": {"Fan": 1, "Bulb": 2, "Mobile Charger": 2, "AC": 1, "LCD/TV": 1, "Laptop Charger": 1},
    "Living Room": {"Fan": 2, "Bulb": 4, "AC": 1, "LCD/TV": 1, "Laptop Charger": 1, "Mobile Charger": 1},
    "Kitchen": {"Oven": 1, "Juicer": 1, "Bulb": 2, "Fridge": 1},
    "Washroom": {"Geyser": 1, "Bulb": 1, "Motor": 1},
    "Laundry Room": {"Washing Machine": 1, "Spinner": 1, "Iron": 1}
}


room_loads = {}
total_load_kw = 0
selected_template = st.selectbox("Select Room Template", ["Custom"] + list(room_templates.keys()))

if selected_template != "Custom":
    st.subheader(f"{selected_template} Configuration")
    appliances = room_templates[selected_template]
    for appliance, quantity in appliances.items():
        appliances[appliance] = st.number_input(f"Number of {appliance}s", min_value=0, value=quantity)
    
    room_load_kw = calculate_total_load(appliances)
    room_loads[selected_template] = room_load_kw
    total_load_kw += room_load_kw
else:
    num_rooms = st.number_input("Number of Rooms", min_value=1, value=1)
    for i in range(1, num_rooms + 1):
        st.subheader(f"Room {i}")
        appliances = {}
        for appliance in appliance_power:
            appliances[appliance] = st.number_input(f"Number of {appliance}s in Room {i}", min_value=0, value=0, help=appliance_descriptions[appliance])
        
        room_load_kw = calculate_total_load(appliances)
        room_loads[f"Room {i}"] = room_load_kw
        total_load_kw += room_load_kw

# Room-wise Output
st.markdown("---")
st.subheader("📊 Room-wise Load Summary")

for room, load_kw in room_loads.items():
    amperes = kw_to_amperes(load_kw)
    breaker = suggest_circuit_breaker(amperes)
    cable = suggest_cable_size(amperes)

    st.write(f"**{room}**")
    st.write(f"🔌 Load: {load_kw:.2f} kW ({amperes:.2f} A)")
    st.write(f"🧯 Suggested Circuit Breaker: {breaker}")
    st.write(f"📦 Suggested Cable Size: {cable}")

    if amperes > 30:
        st.warning("⚠️ Load exceeds 30A — consider splitting into multiple circuits.")

# Total Load Summary
st.markdown("---")
total_amperes = kw_to_amperes(total_load_kw)
main_breaker = suggest_circuit_breaker(total_amperes)
main_cable = suggest_cable_size(total_amperes)
monthly_cost = calculate_energy_cost(total_load_kw, cost_per_kwh=unit_cost)

st.subheader("📌 Total Summary")
st.write(f"💡 Total Load: {total_load_kw:.2f} kW ({total_amperes:.2f} A)")
st.write(f"🛡️ Main Circuit Breaker: {main_breaker}")
st.write(f"🔗 Main Cable Size: {main_cable}")
st.write(f"💸 Estimated Monthly Energy Cost: ₨{monthly_cost:.2f} (at ₨{unit_cost:.2f}/unit)")

 

     
