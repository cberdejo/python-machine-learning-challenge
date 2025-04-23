import streamlit as st
import httpx
from dotenv import load_dotenv
import os

from visualization.api_calls import fetch_models_from_api, predict, train_model


# Load environment variables from .env file
load_dotenv()

API_BASE = f"{os.getenv('HOST', '0.0.0.0')}/api/v1/mpc"

st.set_page_config(page_title="Animal Predictor", layout="centered")

# --- NAVBAR ---
section = st.radio(
    "Navigation",
    ["Train Model", "Predict", "History"],
    horizontal=True,
    label_visibility="collapsed"
)

# --- TRAIN SECTION ---
if section == "Train Model":
    st.title("Train a Model")
    st.session_state.is_training = False
    seed = st.number_input("Seed", min_value=0, value=42)
    num_datapoints = st.number_input("Number of datapoints", min_value=1, value=1000)

    if not st.session_state.is_training:
        if st.button(" Train"):
            st.session_state.is_training = True
            st.rerun()

    if st.session_state.is_training:
        with st.spinner("Training model..."):
            try:
                train_model(seed, num_datapoints, API_BASE)
                st.success("Model trained successfully.")
            except Exception as e:
                st.error(f"Error during training: {e}")
            finally:
                st.session_state.is_training = False
                st.rerun()

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
                entry["walks_on_n_legs"] = st.number_input("Number of legs", value=entry["walks_on_n_legs"], key=f"legs_{idx}")
                entry["height"] = st.number_input("Height (m)", value=entry["height"], step=0.1, key=f"height_{idx}")
                entry["weight"] = st.number_input("Weight (kg)", value=entry["weight"], step=0.1, key=f"weight_{idx}")
                entry["has_wings"] = st.checkbox("Has wings?", value=entry["has_wings"], key=f"wings_{idx}")
                entry["has_tail"] = st.checkbox("Has tail?", value=entry["has_tail"], key=f"tail_{idx}")

                if st.button(f"🗑 Remove Animal", key=f"remove_{idx}"):
                    st.session_state.to_remove = idx
                    st.rerun()
        
        # Añadir un nuevo animal
        if st.button("Add another animal"):
            st.session_state.animal_entries.append({
                "walks_on_n_legs": 4,
                "height": 0.5,
                "weight": 5.0,
                "has_wings": False,
                "has_tail": True
            })
            st.rerun()

        if st.session_state.animal_entries:
            if st.button("Predict"):
                predict(selected_model, API_BASE)


# --- HISTORY SECTION ---
elif section == "History":
    st.title("Prediction History")
    st.info("This section will show all past predictions once the endpoint `/api/v1/mpc/history` is implemented.")
    st.warning("Not implemented yet.")