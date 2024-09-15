from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'services', 'date', 'time']  # Match model field names
        widgets = {
            'date': forms.SelectDateWidget(),  # Custom widget for date selection
            'time': forms.TimeInput(format='%H:%M'),  # Custom widget for time input
        }

    # If services is a ManyToManyField, use ModelMultipleChoiceField
    services = forms.ModelMultipleChoiceField(
        queryset=Booking.objects.all(),  # Adjust the queryset to the correct model if needed
        widget=forms.CheckboxSelectMultiple,  # Display services as checkboxes
        required=True  # Ensure the field is required
    )
