from django.urls import path
from . import views

urlpatterns = [
    path('', views.prediction_form, name='prediction_form'),  # Home page
    path('predict/', views.predict, name='predict'),  # Prediction endpoint
]
