import pickle

try:
    # Test loading the model
    with open('predictor/model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    print("Model loaded successfully")

    # Test loading the scaler
    with open('predictor/scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    print("Scaler loaded successfully")

except pickle.UnpicklingError as e:
    print(f"Unpickling error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
