from account.models import Education
from account.models import User
from django import forms


class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    remember = forms.BooleanField(label="Remember me", required=False)


class UserRegisterForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password2", widget=forms.PasswordInput)
    employer = forms.BooleanField(label="Employer", required=False)

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
        is_employer = self.cleaned_data.get("employer")
        user = User.objects.create_user(
            username=username, email=email, password=password, is_employer=is_employer
        )
        return user


class UserSettingsForm(forms.Form):
    instance = None

    first_name = forms.CharField(label="First name", max_length=255, required=False)
    last_name = forms.CharField(label="Last name", max_length=255, required=False)
    patronymic = forms.CharField(label="Patronymic", max_length=255, required=False)
    phone_number = forms.CharField(label="Phone number", max_length=255, required=False)
    address = forms.CharField(label="Address", max_length=255, required=False)
    avatar = forms.ImageField(label="Avatar", required=False)
    user_site = forms.CharField(label="User site", max_length=255, required=False)
    user_github = forms.CharField(label="User github", max_length=255, required=False)
    user_twitter = forms.CharField(label="User twitter", max_length=255, required=False)
    user_instagram = forms.CharField(
        label="User instagram", max_length=255, required=False
    )
    user_facebook = forms.CharField(
        label="User facebook", max_length=255, required=False
    )

    class Meta:
        model = User

    def save(self, commit=True) -> User:
        user = self.instance
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.patronymic = self.cleaned_data.get("patronymic")
        user.phone_number = self.cleaned_data.get("phone_number")
        user.address = self.cleaned_data.get("address")
        user.user_site = self.cleaned_data.get("user_site")
        user.user_github = self.cleaned_data.get("user_github")
        user.user_twitter = self.cleaned_data.get("user_twitter")
        user.user_instagram = self.cleaned_data.get("user_instagram")
        user.user_facebook = self.cleaned_data.get("user_facebook")

        user.save()
        return user


class UserEducationForm(forms.Form):
    instance = None
    institution = forms.CharField(label="Institution", max_length=255, required=True)
    faculty = forms.CharField(label="Faculty", max_length=255, required=True)
    speciality = forms.CharField(label="Speciality", max_length=255, required=True)
    start_date = forms.DateField(label="Start date", required=True)
    end_date = forms.DateField(label="End date", required=True)
    degree = forms.ChoiceField(choices=Education.DEGREES, required=True)
    description = forms.CharField(
        label="Description", required=True, widget=forms.Textarea
    )

    def save(self, commit=True):
        if getattr(self, "instance", None) is None:
            raise ValueError("Can't update education")
        user = self.instance
        if getattr(user, "education", None) is None:
            user.education = Education()
        user.education.institution = self.cleaned_data.get("institution")
        user.education.faculty = self.cleaned_data.get("faculty")
        user.education.speciality = self.cleaned_data.get("speciality")
        user.education.start_date = self.cleaned_data.get("start_date")
        user.education.end_date = self.cleaned_data.get("end_date")
        user.education.degree = self.cleaned_data.get("degree")
        user.education.description = self.cleaned_data.get("description")
        user.education.save()
        return user.education


class UserSecurityForm(forms.Form):
    instance = None

    def save(self, commit=False):
        if getattr(self, "instance", None) is None:
            raise ValueError("Can't update security, user is None")
        user = self.instance
        user.save()
        return user


class PasswordChangeForm(forms.Form):
    instance = None
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password2", widget=forms.PasswordInput)

    def clean_password2(self) -> str:
        password = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Password mismatch")
        return password2

    def save(self, commit=True) -> User:
        if getattr(self, "instance", None) is None:
            raise ValueError("Can't update password, user is None")
        user: User = self.instance
        user.set_password(self.cleaned_data.get("password1"))
        user.save()
        return user
