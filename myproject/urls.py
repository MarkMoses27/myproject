# myproject/urls.py
from django.contrib import admin
from django.urls import path
from emails.views import booking_form

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', booking_form, name='booking_form'),
]
