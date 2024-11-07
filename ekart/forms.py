from django import forms
from .models import User,EndUser

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

class PaymentForm(forms.Form):
    order_id = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    total_price=forms.IntegerField()
    contact_number = forms.CharField(max_length=15)
    pincode = forms.CharField(max_length=10)
    street_address = forms.CharField(max_length=255, label="Street Address")
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if not contact_number.isdigit() or len(contact_number) < 10:
            raise forms.ValidationError("Invalid contact number.")
        return contact_number

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if not pincode.isdigit() or len(pincode) != 6:
            raise forms.ValidationError("Invalid pincode.")
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
        
class PaymentForm(forms.Form):
    order_id = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        label="Order ID"  # Added label for clarity
    )
    total_price = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        widget=forms.TextInput(attrs={'readonly': 'readonly'})  # Make total_price read-only if it's calculated
    )
    contact_number = forms.CharField(
        max_length=15, 
        label="Contact Number"
    )
    pincode = forms.CharField(
        max_length=10, 
        label="Pincode"
    )
    street_address = forms.CharField(
        max_length=255, 
        label="Street Address"
    )
    city = forms.CharField(
        max_length=100, 
        label="City"
    )
    state = forms.CharField(
        max_length=100, 
        label="State"
    )

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if not contact_number.isdigit() or len(contact_number) < 10:
            raise forms.ValidationError("Invalid contact number. It should be numeric and at least 10 digits.")
        return contact_number

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if not pincode.isdigit() or len(pincode) != 6:
            raise forms.ValidationError("Invalid pincode. It should be numeric and exactly 6 digits.")
        return pincode