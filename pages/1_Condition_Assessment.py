import streamlit as st
from rules.decision_engine import assess_item

st.set_page_config(
    page_title="EcoSort Edge - Assessment",
    page_icon="♻️"
)

st.title("♻️ E-Waste Condition Assessment")

st.write("Tell us about your electronic item.")

item = st.selectbox(
    "1. Select your electronic item",
    [
        "Mobile Phone",
        "Tablet",
        "Charger / Adapter",
        "Cable",
        "Circuit Board",
        "Computer Accessory",
        "Other E-Waste"
    ]
)

working = st.radio(
    "2. Does the item work?",
    ["Yes", "No", "Not sure"]
)

damage = st.selectbox(
    "3. What damage is visible?",
    [
        "No visible damage",
        "Cracked or broken parts",
        "Burn marks",
        "Corrosion",
        "Other damage",
        "Not sure"
    ]
)

battery = st.radio(
    "4. Is the battery swollen or leaking?",
    ["No", "Yes", "Not sure", "Not applicable"]
)

if st.button("Submit Assessment"):

    st.session_state["assessment"] = {
        "Item": item,
        "Working condition": working,
        "Visible damage": damage,
        "Battery condition": battery
    }

    if battery == "Yes":
        st.error(
            "Safety warning: Do not charge, dismantle "
            "or handle a swollen or leaking battery. "
            "Seek professional handling."
        )

    st.success("Assessment submitted successfully!")

    st.json(st.session_state["assessment"])
    result = assess_item(st.session_state["assessment"])

    st.subheader("EcoSort Edge Recommendation")

    st.write("Status:", result["status"])
    st.write("Recommended action:", result["recommendation"])
    st.info(result["message"])