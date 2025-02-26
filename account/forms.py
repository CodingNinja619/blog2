from django import forms
from blog.models import User
from django.forms import ValidationError
class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput())


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email"]
        help_texts = {
            "username": "Required. 150 characters maximum. Letters, digits and @/./+/-/_ only."
        }
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password2"] != cd["password1"]:
            raise ValidationError("Passwords don't match.")
        else:
            return cd["password2"]