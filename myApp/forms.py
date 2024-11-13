from django import forms
from .models import Attendee

class AttendeeRegistrationForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['first_name', 'last_name', 'middle_initial', 'nickname', 'mobile_number']

    # Add CSS classes and placeholders for the fields
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'})
    )
    middle_initial = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your middle initial (optional)'}),
        required=False  # This is optional, so it should not be required
    )
    nickname = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your nickname (Required)'}),
        required=False  # This is optional, so it should not be required
    )
    mobile_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your mobile number (optional)'}),
        required=False,  # This is optional, so it should not be required
    )
    
