import streamlit as st
import pandas as pd
import json

from pathlib import Path
from PIL import Image

from llama_helper import generate_ewaste_guidance
from rules.decision_engine import assess_item
from vision.predict import load_model, predict_image, suggest_category


# ========================================
# PROJECT CONFIGURATION
# ========================================

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_FILE = BASE_DIR / "knowledge_base" / "ewaste_guidance.json"

st.set_page_config(
    page_title="EcoSort Edge",
    page_icon="♻️",
    layout="wide"
)


# ========================================
# SESSION STATE
# ========================================

session_defaults = {
    "history": [],
    "last_result": None,
    "last_assessment": None,
    "llama_response": None,
    "prediction": None,
    "response_time": None,
    "suggested_category": None,
    "current_filename": None
}

for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ========================================
# LOAD AI MODEL
# ========================================

@st.cache_resource
def get_ai_model():
    return load_model()


# ========================================
# LOAD KNOWLEDGE BASE
# ========================================

@st.cache_data
def load_knowledge_base():
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_knowledge_key(category):

    category_map = {
        "Mobile / Tablet": "mobile_tablet",
        "Charger / Adapter": "charger_adapter",
        "Cable": "cable",
        "Circuit Board": "circuit_board",
        "Computer Accessory": "computer_accessory",
        "Other E-waste": "other_ewaste"
    }

    return category_map.get(category)


# ========================================
# APPLICATION HEADER
# ========================================

st.title("♻️ EcoSort Edge")

st.subheader(
    "AI-Powered E-Waste Identification, "
    "Condition Assessment and Recycling Assistant"
)

st.write(
    "Upload an electronic item photograph, "
    "confirm its condition and receive "
    "responsible e-waste handling guidance."
)

st.divider()


# ========================================
# STEP 1: IMAGE UPLOAD
# ========================================

st.header("1. Upload Electronic Waste Image")

uploaded_file = st.file_uploader(
    "Upload an electronic item photograph",
    type=["jpg", "jpeg", "png"]
)

category_options = [
    "Mobile / Tablet",
    "Charger / Adapter",
    "Cable",
    "Circuit Board",
    "Computer Accessory",
    "Other E-waste"
]


if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded electronic item",
        width=350
    )

    # Reset results when a different image is uploaded
    image_bytes = uploaded_file.getvalue()

    if st.session_state["current_filename"] != (
        uploaded_file.name + str(hash(image_bytes))
    ):

        st.session_state["current_filename"] = (
            uploaded_file.name + str(hash(image_bytes))
        )

        st.session_state["last_result"] = None
        st.session_state["last_assessment"] = None
        st.session_state["llama_response"] = None
        st.session_state["prediction"] = None
        st.session_state["response_time"] = None
        st.session_state["suggested_category"] = None

    st.divider()


    # ========================================
    # STEP 2: AI IMAGE PREDICTION
    # ========================================

    st.header("2. AI Image Prediction")

    if st.session_state["prediction"] is None:

        try:

            with st.spinner("Loading AI model and analysing image..."):

                model, preprocess, categories = get_ai_model()

                predictions, response_time = predict_image(
                    image,
                    model,
                    preprocess,
                    categories
                )

                suggested = suggest_category(
                    predictions[0]["label"]
                )

                st.session_state["prediction"] = predictions
                st.session_state["response_time"] = response_time
                st.session_state["suggested_category"] = suggested

        except Exception as error:

            st.error("Image prediction failed.")
            st.exception(error)

    if st.session_state["prediction"] is not None:

        predictions = st.session_state["prediction"]

        st.metric(
            "AI Processing Time",
            f"{st.session_state['response_time']:.2f} ms"
        )

        st.write("**Top 3 model predictions:**")

        for prediction in predictions:

            st.write(
                f"- {prediction['label']} "
                f"({prediction['confidence'] * 100:.2f}%)"
            )

        suggested = st.session_state["suggested_category"]

        st.info(f"Suggested category: {suggested}")

        st.caption(
            "Predictions are generated by your trained "
            "MobileNetV3 e-waste classification model. "
            "Please confirm the category manually."
        )

    else:

        st.warning(
            "Prediction is unavailable. Please check the model "
            "and try uploading the image again."
        )

        st.stop()

    st.divider()


    # ========================================
    # STEP 3: NON-E-WASTE DETECTION
    # ========================================

    if suggested == "Non-E-waste":

        st.error(
            "This image appears to be NON-E-WASTE."
        )

        st.warning(
            "Please upload an electronic waste image "
            "to continue with EcoSort Edge."
        )

        st.stop()


    # ========================================
    # STEP 4: CONFIRM E-WASTE CATEGORY
    # ========================================

    st.header("3. Confirm E-Waste Category")

    default_index = (
        category_options.index(suggested)
        if suggested in category_options
        else 0
    )

    selected_category = st.selectbox(
        "Select the correct electronic item category:",
        category_options,
        index=default_index
    )

    st.caption(
        "The AI prediction is a suggestion. "
        "Please confirm the correct category."
    )

    st.divider()


    # ========================================
    # STEP 5: CONDITION ASSESSMENT
    # ========================================

    st.header("4. Condition Assessment")

    working = st.radio(
        "Does the item work?",
        ["Yes", "No", "Not sure"],
        key="working_condition"
    )

    damage = st.selectbox(
        "What visible damage is present?",
        [
            "No visible damage",
            "Cracked or broken",
            "Exposed wires",
            "Burn marks",
            "Corrosion or rust",
            "Other visible damage"
        ],
        key="visible_damage"
    )

    battery = st.radio(
        "Is the battery swollen or leaking?",
        ["No", "Yes", "Not sure", "Not applicable"],
        key="battery_condition"
    )

    st.divider()


    # ========================================
    # STEP 6: ANALYSE ELECTRONIC ITEM
    # ========================================

    st.header("5. Analyse Electronic Item")

    if st.button(
        "Analyse and Get Recommendation",
        type="primary",
        use_container_width=True
    ):

        assessment = {
            "Item": selected_category,
            "Working condition": working,
            "Visible damage": damage,
            "Battery condition": battery
        }

        try:

            result = assess_item(assessment)

            st.session_state["last_assessment"] = assessment
            st.session_state["last_result"] = result

            st.session_state["llama_response"] = None

            history_entry = {
                "Item": selected_category,
                "Working": working,
                "Damage": damage,
                "Battery": battery,
                "Status": result["status"],
                "Recommendation": result["recommendation"]
            }

            st.session_state["history"].append(history_entry)

            st.success(
                "Electronic item analysed successfully!"
            )

        except Exception as error:

            st.error("Assessment failed.")
            st.exception(error)


    # ========================================
    # STEP 7: DISPLAY RESULT
    # ========================================

    if st.session_state["last_result"] is not None:

        result = st.session_state["last_result"]
        assessment = st.session_state["last_assessment"]

        st.divider()

        st.header("6. EcoSort Edge Result")

        st.write(
            "**Identified category:**",
            assessment["Item"]
        )

        st.write(
            "**Working condition:**",
            assessment["Working condition"]
        )

        st.write(
            "**Visible damage:**",
            assessment["Visible damage"]
        )

        st.write(
            "**Battery condition:**",
            assessment["Battery condition"]
        )

        st.write("**Status:**", result["status"])

        st.write(
            "**Recommended action:**",
            result["recommendation"]
        )

        if (
            "WARNING" in result["status"]
            or "SAFETY" in result["status"]
        ):

            st.error(result["message"])

        elif result["status"] == "ASSESSMENT NEEDED":

            st.warning(result["message"])

        else:

            st.info(result["message"])

        st.caption(
            "This is preliminary guidance based on "
            "user-provided information, not a technical "
            "device diagnosis."
        )


        # ========================================
        # STEP 8: LLAMA AI E-WASTE ADVISOR
        # ========================================

        st.divider()

        st.header("🦙 7. Llama AI E-Waste Advisor")

        st.write(
            "Generate personalised e-waste handling and "
            "recycling guidance using your locally installed "
            "Llama 3.2 1B model."
        )

        st.caption(
            "Llama generates additional guidance based on "
            "the item and its assessment."
        )

        if st.button(
            "🦙 Generate AI E-Waste Advice",
            type="primary",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "Llama is generating your e-waste guidance..."
                ):

                    llama_response = generate_ewaste_guidance(
                        assessment["Item"],
                        assessment["Working condition"],
                        assessment["Visible damage"],
                        assessment["Battery condition"],
                        (
                            result["status"]
                            + ": "
                            + result["recommendation"]
                            + ". "
                            + result["message"]
                        )
                    )

                    st.session_state["llama_response"] = llama_response

            except Exception as error:

                st.error("Llama AI guidance generation failed.")
                st.exception(error)

        if st.session_state["llama_response"]:

            st.subheader("AI-Generated Recommendation")

            st.markdown(
                st.session_state["llama_response"]
            )

            st.caption(
                "AI-generated guidance is supplementary. "
                "Follow safety warnings and consult a qualified "
                "technician when necessary."
            )


        # ========================================
        # STEP 9: KNOWLEDGE BASE GUIDANCE
        # ========================================

        st.divider()

        st.header("8. Local Knowledge Base Guidance")

        try:

            knowledge = load_knowledge_base()

            key = get_knowledge_key(assessment["Item"])

            if key and key in knowledge:

                guidance = knowledge[key]

                st.subheader("Recommended Guidance")

                st.write("**Reuse:**", guidance["reuse"])
                st.write("**Repair:**", guidance["repair"])
                st.write("**Recycling:**", guidance["recycle"])
                st.write("**Safety:**", guidance["safety"])

                if "data_protection" in guidance:

                    st.write(
                        "**Data protection:**",
                        guidance["data_protection"]
                    )

                st.caption(
                    "Source status: " + guidance["source"]
                )

                st.caption(
                    "Verification date: "
                    + str(guidance.get("verification_date"))
                )

                st.caption(
                    "Knowledge-base entries require "
                    "official source verification."
                )

            else:

                st.warning(
                    "No guidance found for this category."
                )

        except Exception as error:

            st.error(
                "Could not load the local knowledge base."
            )

            st.caption(str(error))


else:

    st.info(
        "Upload an electronic waste photograph to begin."
    )


# ========================================
# STEP 10: ASSESSMENT HISTORY
# ========================================

st.divider()

st.header("9. Assessment History")

if st.session_state["history"]:

    history_df = pd.DataFrame(
        st.session_state["history"]
    )

    st.dataframe(
        history_df,
        use_container_width=True
    )

    csv_data = history_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Assessment Report",
        data=csv_data,
        file_name="EcoSort_Edge_Assessment_Report.csv",
        mime="text/csv"
    )

else:

    st.info("No assessment history available yet.")


# ========================================
# ABOUT PROJECT
# ========================================

st.divider()

st.header("About EcoSort Edge")

st.write(
    "EcoSort Edge is an AI-assisted e-waste management "
    "application that combines image recognition, manual "
    "condition assessment, a Python decision engine, a local "
    "knowledge base and Llama AI-generated guidance."
)

st.write(
    "Its objective is to support responsible electronic "
    "waste handling through reuse, repair, recycling "
    "and professional safety guidance."
)

st.caption(
    "EcoSort Edge | Bharat AI-SoC Challenge | PS2"
)