from django import forms
from .models import EndUser,Order

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = EndUser
        fields = ['email', 'password']  # Ensure 'email' is in your model

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if EndUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
    
class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'total_price', 'contact_number', 'alternate_contact_number', 'pincode', 'street_address', 'city', 'state'
        ]
        widgets = {
            'street_address': forms.TextInput(attrs={'placeholder': 'Enter your street address'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
            'contact_number': forms.TextInput(attrs={'placeholder': 'Contact Number'}),
            'alternate_contact_number': forms.TextInput(attrs={'placeholder': 'Alternate Contact Number'}),
            'pincode': forms.TextInput(attrs={'placeholder': '6-digit Pincode'}),
            'total_price': forms.NumberInput(attrs={'placeholder': 'Total Price'}),
        }

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if not contact_number.isdigit() or len(contact_number) < 10:
            raise forms.ValidationError("Invalid contact number. It must be at least 10 digits.")
        return contact_number

    def clean_alternate_contact_number(self):
        alternate_contact_number = self.cleaned_data.get('alternate_contact_number')
        if alternate_contact_number:  # Validate only if an alternate contact number is provided
            if not alternate_contact_number.isdigit() or len(alternate_contact_number) < 10:
                raise forms.ValidationError("Invalid alternate contact number. It must be at least 10 digits.")
        return alternate_contact_number

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if not pincode.isdigit() or len(pincode) != 6:
            raise forms.ValidationError("Pincode must be a 6-digit number.")
        return pincode

# forms.py

from django import forms

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email Address')

class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        