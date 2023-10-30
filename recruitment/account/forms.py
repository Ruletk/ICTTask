from account.models import User
from django import forms


class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            return user
        else:
            raise forms.ValidationError("Invalid email or password")


class UserRegisterForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password2", widget=forms.PasswordInput)

    class Meta:
        model = User

    def clean_email(self) -> str:
        email = self.cleaned_data.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            raise forms.ValidationError("This email already exists")
        return email

    def clean_password2(self) -> str:
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Password mismatch")
        return password2

    def save(self, commit=True) -> User:
        username = self.cleaned_data.get("email").split("@")[0]
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        return user
