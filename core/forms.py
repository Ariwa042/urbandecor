# core/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re
from .models import ContactMessage
from .models import NewsletterSubscriber

class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
        }
# User Sign-Up Form (Email + Password only)
class UserSignupForm(forms.Form):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        error_messages={'invalid': 'Please enter a valid email address.'}
    )
    password = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        min_length=6,  # Password minimum length
        error_messages={'min_length': 'Password must be at least 8 characters long.'}
    )

    # Custom validators
    def clean_email(self):
        email = self.cleaned_data['email']
        # Check if the email is already registered
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError('This email is already registered. login instead')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        # Password validation: Ensure it contains at least one number, one uppercase letter
#        if not re.search(r'[A-Z]', password):
 #           raise ValidationError('Password must contain at least one uppercase letter.')
        return password


# User Login Form (Email + Password only)
class UserLoginForm(forms.Form):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        error_messages={'invalid': 'Please enter a valid email address.'}
    )
    password = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )


# Contact Message Form
class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Your Name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Your Email'})
        self.fields['subject'].widget.attrs.update({'placeholder': 'Subject'})
        self.fields['message'].widget.attrs.update({'placeholder': 'Your Message'})

