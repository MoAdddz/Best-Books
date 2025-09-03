from django import forms
from django.core.exceptions import ValidationError
from .models import User  # Make sure this import is correct for your project

# This is a form that helps people sign up for your website.
# It collects information like username, email, and password.
class MyUserRegistrationForm(forms.ModelForm):
    # This field asks the user to type their username.
    # max_length=30 means the username can't be longer than 30 letters.
    username = forms.CharField(max_length=30, label="Username", required=True, strip=True)
    # This field asks for the user's email address.
    email = forms.EmailField(label="Email", required=True)
    # This field asks for a password. The input will be hidden (like dots or stars).
    password = forms.CharField(widget=forms.PasswordInput, label="Password", required=True, strip=True)
    # This field asks the user to type their password again to make sure they didn't make a mistake.
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password", required=True, strip=True)

    # This class tells Django which database model this form is for.
    class Meta:
        # We are using the User model, which stores information about users.
        model = User
        # These are the fields we want to show in the form.
        fields = ['username', 'email', 'password', 'confirm_password']
    
    # This function checks if the passwords match.
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        # If the passwords don't match, raise a ValidationError.
        if password != confirm_password:
            raise ValidationError("Passwords do not match.")
        
        if password and len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if username and User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists. Please choose a different one.")
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists. Please choose a different one.")
        return cleaned_data
    
    def save(self, commit=True):
        # This function saves the user data to the database.
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class MyLoginForm(forms.Form):
    # This field asks for the user's username.
    username = forms.CharField(max_length=30, label="Username", required=True, strip=True, help_text="Enter your username")
    # This field asks for the user's password. The input will be hidden (like dots or stars).
    password = forms.CharField(widget=forms.PasswordInput, label="Password", required=True, strip=True, help_text="Enter your password.")
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not username or not password:
            raise ValidationError("Both fields are required.")
        
        return cleaned_data