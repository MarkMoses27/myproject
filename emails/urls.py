from django.urls import path
from .views import booking_form

urlpatterns = [
    path('api/book/', booking_form),  # Booking form API endpoint with trailing slash
]
