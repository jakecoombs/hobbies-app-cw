from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=50,
        widget=forms.TextInput(attrs={"autocomplete": "username"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"autocomplete": "password"})
    )

class SignupForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=50,
        widget=forms.TextInput(attrs={"autocomplete": "username"})
    )
    email = forms.CharField(
        label="Email",
        max_length=50,
        widget=forms.TextInput(attrs={"autocomplete": "email"})
    )
    dob = forms.DateField(
        label="Date of birth",
        widget=forms.DateInput(attrs={"type": "date"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"autocomplete": "password"})
    )
    password_confirmation = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput()
    )

class HobbyForm(forms.Form):
    name = forms.CharField(
        label="Name",
        max_length=50,
        widget=forms.TextInput(attrs={"autocomplete": "name"})
    )
    description = forms.CharField(
        label="Description",
        max_length=200,
        widget=forms.TextInput(attrs={"autocomplete": "description"})
    )