from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "enter name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder": "enter email"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder": "enter conttt"}))

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if "gmail.com" not in email:
            raise forms.ValidationError("ایمیل باید gmail.com باشد")
        return email

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "enter name"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "enter pass"})
    )

class RegisterForm(forms.Form):
        username = forms.CharField(
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "enter name"})
        )
        email = forms.EmailField(
            widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "enter email"}))

        password = forms.CharField(
            widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "enter pass"})
        )

        password2 = forms.CharField(
            label="Confirm Password",
            widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "enter pass again"})
        )

        def clean_userName(self):
            userName = self.cleaned_data.get("userName")
            qs = User.objects.filter(userName=userName)
            if qs.exists():
                raise forms.ValidationError("username is taken")
            return userName

        def clean_email(self):
            email = self.cleaned_data.get("email")
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("email is taken")
            return email


        def clean(self):
            data = self.cleaned_data
            password = self.cleaned_data.get("password")
            password2 = self.cleaned_data.get("password2")

            if password != password2:
                raise forms.ValidationError("passwords not correct")
            return data