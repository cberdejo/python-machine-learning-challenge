import streamlit as st
import httpx
from dotenv import load_dotenv
import os

from visualization.api_calls import fetch_history, fetch_models_from_api, predict, train_model


# Load environment variables from .env file
load_dotenv()

API_BASE = f"{os.getenv('HOST', '0.0.0.0')}/api/v1/mpc"

st.set_page_config(page_title="Animal Predictor", layout="centered")
# --- NAVBAR ---

if "is_training" not in st.session_state:
    st.session_state.is_training = False
if "training_result" not in st.session_state:
    st.session_state.training_result = None

# Forzar vista "Train Model" durante entrenamiento
if st.session_state.is_training:
    section = "Train Model"
else:
    section = st.radio(
        "Navigation",
        ["Train Model", "Predict", "History"],
        horizontal=True,
        label_visibility="collapsed",
    )

# --- TRAIN SECTION ---
if section == "Train Model":
    st.title("Train a Model")
    seed = st.number_input("Seed", min_value=0, value=42)
    num_datapoints = st.number_input("Number of datapoints", min_value=1, value=1000)

    if st.button(" Train") and not st.session_state.is_training:
        st.session_state.is_training = True
        st.session_state.training_result = None
        st.rerun()  

    if st.session_state.is_training and st.session_state.training_result is None:
        with st.spinner("Training model..."):
            result = train_model(seed, num_datapoints, API_BASE)
            st.session_state.training_result = result
            st.session_state.is_training = False
            st.rerun()

    # Mostrar resultado tras el entrenamiento
    if st.session_state.training_result:
        result = st.session_state.training_result
        if result["success"]:
            st.success(" Model trained successfully.")
            st.json(result["data"])
        else:
            st.error(f" Training failed: {result['error']}")


# --- PREDICT SECTION ---
elif section == "Predict":
    st.title("Predict Animal Labels")

    available_models = fetch_models_from_api(API_BASE)

    if not available_models:
        st.info("In order to predict, you need to train a model.")
    else:
        selected_model = st.selectbox("Select a model", options=available_models)

        st.subheader("Input Animal Data")

        if "animal_entries" not in st.session_state:
            st.session_state.animal_entries = []

        # Eliminar entrada
        to_remove = st.session_state.get("to_remove", None)
        if to_remove is not None:
            del st.session_state.animal_entries[to_remove]
            st.session_state.to_remove = None
            st.rerun()

        # Renderizar entradas
        for idx, entry in enumerate(st.session_state.animal_entries):
            with st.expander(f"Animal {idx + 1}", expanded=True):
                entry["walks_on_n_legs"] = st.number_input(
                    "Number of legs", value=entry["walks_on_n_legs"], key=f"legs_{idx}"
                )
                entry["height"] = st.number_input(
                    "Height (m)", value=entry["height"], step=0.1, key=f"height_{idx}"
                )
                entry["weight"] = st.number_input(
                    "Weight (kg)", value=entry["weight"], step=0.1, key=f"weight_{idx}"
                )
                entry["has_wings"] = st.checkbox(
                    "Has wings?", value=entry["has_wings"], key=f"wings_{idx}"
                )
                entry["has_tail"] = st.checkbox(
                    "Has tail?", value=entry["has_tail"], key=f"tail_{idx}"
                )

                if st.button(f"🗑 Remove Animal", key=f"remove_{idx}"):
                    st.session_state.to_remove = idx
                    st.rerun()

        # Añadir un nuevo animal
        if st.button("Add another animal"):
            st.session_state.animal_entries.append(
                {
                    "walks_on_n_legs": 4,
                    "height": 0.5,
                    "weight": 5.0,
                    "has_wings": False,
                    "has_tail": True,
                }
            )
            st.rerun()

        if st.session_state.animal_entries:
            if st.button("Predict"):
                predict(selected_model, API_BASE)


# --- HISTORY SECTION ---
elif section == "History":
    st.title("Prediction History")
    st.subheader("Filter by Date Range")

    start_date = st.date_input("Start date")
    end_date = st.date_input("End date")

    if st.button("Fetch History"):
        params = {}
        if start_date:
            params["start"] = start_date.isoformat()
        if end_date:
            params["end"] = end_date.isoformat()

        result = fetch_history(API_BASE, params)

        if result["success"]:
            data = result["data"]
            if data["code"] == 200:
                predictions = data["data"]
                if not predictions:
                    st.info("No predictions found for the selected date range.")
                else:
                    for pred in predictions:
                        st.markdown(f"###  Date: `{pred['date']}`")
                        st.table(pred["animal_data"])
            else:
                st.warning(f" {data['message']}")
        else:
            st.error(f" Error fetching prediction history: {result['error']}")
