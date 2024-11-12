from django.shortcuts import render
from django.http import HttpResponse
import pickle
import os
from django.conf import settings
import numpy as np
from sklearn.exceptions import NotFittedError

# Load the ML model and the scaler
model_path = os.path.join(settings.BASE_DIR, 'predictor/model.pkl')
scaler_path = os.path.join(settings.BASE_DIR, 'predictor/scaler.pkl')

with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

with open(scaler_path, 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

def prediction_form(request):
    """Render the form for user input."""
    return render(request, 'predictor/prediction_form.html')


def predict(request):
    """Handle form submission and redirect to results page."""
    if request.method == 'POST':
        # Get data from the form
        age = int(request.POST.get('age'))
        resting_bp = int(request.POST.get('resting_bp'))
        cholesterol = int(request.POST.get('cholesterol'))
        fasting_bs = int(request.POST.get('fasting_bs'))
        max_hr = int(request.POST.get('max_hr'))
        oldpeak = float(request.POST.get('oldpeak'))
        sex_m = request.POST.get('sex_m') == 'on'
        chestpain_ata = request.POST.get('chestpain_ata') == 'on'
        chestpain_nap = request.POST.get('chestpain_nap') == 'on'
        chestpain_ta = request.POST.get('chestpain_ta') == 'on'
        resting_ecg_normal = request.POST.get('resting_ecg_normal') == 'on'
        resting_ecg_st = request.POST.get('resting_ecg_st') == 'on'
        exercise_angina_y = request.POST.get('exercise_angina_y') == 'on'
        st_slope_flat = request.POST.get('st_slope_flat') == 'on'
        st_slope_up = request.POST.get('st_slope_up') == 'on'

        # Prepare the feature array
        features = np.array([[
            age, resting_bp, cholesterol, fasting_bs, max_hr, oldpeak,
            sex_m, chestpain_ata, chestpain_nap, chestpain_ta,
            resting_ecg_normal, resting_ecg_st, exercise_angina_y,
            st_slope_flat, st_slope_up
        ]])

        # Check if the scaler is fitted, if not, fit it with some sample data
        try:
            features_scaled = scaler.transform(features)
        except NotFittedError:
            # Fitting the scaler with the feature itself (you can use original training data)
            scaler.fit(features)
            features_scaled = scaler.transform(features)

        # Make the prediction
        prediction = model.predict(features_scaled)
        result = "Heart Disease Detected" if prediction[0] == 1 else "No Heart Disease Detected"

        # Render the result page
        return render(request, 'predictor/prediction_result.html', {'result': result})

    return render(request, 'predictor/prediction_form.html')
