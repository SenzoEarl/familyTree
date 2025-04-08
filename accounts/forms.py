from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile, Address, ContactInfo


# Form for creating a new user (registration)
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = [ 'username', 'password1', 'password2']


# Form for updating the profile information
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'bio']


# Form for handling address information
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_address', 'city', 'state', 'postal_code', 'country']


# Form for handling contact information
class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['phone_number', 'alternate_email']

