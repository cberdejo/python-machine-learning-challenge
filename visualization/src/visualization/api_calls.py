
import streamlit as st
import httpx



@st.cache_data(ttl=300)  # cache por 5 minutos (ajustable)
def fetch_models_from_api(api_base: str) -> list:
    """
    Fetches the list of models from the API.
    Args:
        api_base (str): The base URL of the API.
    Returns:
        list: A list of models.
    """
    try:
        with httpx.Client(timeout=10.0) as client:
            model_response = client.get(f"{api_base}/models")
            model_response.raise_for_status()
            return model_response.json().get("data", [])
    except Exception as e:
        st.error(f"Error fetching models: {e}")
        return []
    

def train_model(seed, num_datapoints, api_base: str) -> None:
    """
    Trains a model using the provided seed and number of datapoints.
    Args:
        seed (int): The seed for the data generation which the model uses to be trained.  
        num_datapoints (int): The number of datapoints for data generation which the model uses to be trained.
        api_base (str): The base URL of the API.
    """
    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(f"{api_base}/train?seed={seed}&number_of_datapoints={num_datapoints}")
            response.raise_for_status()
            print(response.json())  # Debugging line to check the response
            st.success("Model trained successfully!")
            st.json(response.json())
    except Exception as e:
        st.error(f"Error: {e}")
def predict(selected_model: str, api_base: str) -> None:
    """
    Predicts the labels of the animals using the selected model.
    Args:
        selected_model (str): The selected model in the format "seed-number_of_datapoints".
        api_base (str): The base URL of the API.
    """
    try:
        try:
            seed_str, datapoints_str = selected_model.split("-")
            model_params = {
                "seed": int(seed_str),
                "number_of_datapoints": int(datapoints_str)
            }
        except ValueError:
            st.error("Invalid model format. Expected format: seed-number_of_datapoints")
            return

        payload = {
            "model": model_params,
            "data": st.session_state.animal_entries
        }

        with httpx.Client(timeout=10.0) as client:
            response = client.post(f"{api_base}/predict", json=payload)
            response.raise_for_status()
            result = response.json()

            if "data" in result:
                st.success("Prediction results:")
                for i, item in enumerate(result["data"]):
                    st.write(f"Animal {i+1} → Label: **{item.get('label', 'N/A')}**")
            else:
                st.error("Unexpected response format.")
    except Exception as e:
        st.error(f"Error: {e}")
