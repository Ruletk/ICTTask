from datetime import datetime

from django import forms
from jobs.models import Skill
from jobs.models import Vacancy
from jobs.models.Resume import Resume


class SearchJobForm(forms.Form):
    keyword = forms.CharField(max_length=255, required=False)
    location = forms.CharField(max_length=255, required=False)
    salary = forms.FloatField(required=False)


class CreateVacancyForm(forms.ModelForm):
    # title = forms.CharField(max_length=255)
    # description = MartorFormField()
    # salary_min = forms.IntegerField()
    # salary_max = forms.IntegerField()
    # location = forms.CharField(max_length=255)
    working_days = forms.MultipleChoiceField(
        choices=Vacancy.WORKING_DAYS,
        required=False,
        label="...",
        widget=forms.CheckboxSelectMultiple(),
    )
    # experience_time = forms.IntegerField()
    # possibilities = forms.ModelMultipleChoiceField(Possibility.objects.all(), required=False)
    # skills = forms.ModelMultipleChoiceField(Skill.objects.all(), required=False)

    def clean_working_days(self):
        data = self.cleaned_data["working_days"]
        value = 0
        for i in data:
            value += 2 ** (6 - int(i))
        return value

    def save(self, commit=True):
        if not getattr(self, "user"):
            raise ValueError("User is not set")

        if self.user.is_anonymous:
            raise ValueError("User is anonymous")

        if not self.user.is_employer:
            raise ValueError("User is not employer")

        vacancy = super(CreateVacancyForm, self).save(commit=False)

        vacancy.published_at = datetime.now()
        vacancy.company = self.user.company.all()[0]
        if commit:
            vacancy.save()
        return vacancy

    class Meta:
        model = Vacancy
        fields = (
            "title",
            "description",
            "salary_min",
            "salary_max",
            "location",
            "working_days",
            "experience_time",
            "possibilities",
            "skills",
        )


class CreateResumeForm(forms.Form):
    instance = None

    title = forms.CharField(max_length=255)
    salary = forms.FloatField()
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(), required=False
    )
    phone_number = forms.CharField(max_length=20, required=False)
    experience = forms.CharField(widget=forms.Textarea)
    achievements = forms.CharField(widget=forms.Textarea)
    hobbies = forms.CharField(widget=forms.Textarea)
    additional_info = forms.CharField(widget=forms.Textarea)

    def clean_salary(self):
        data = self.cleaned_data["salary"]
        if data < 0:
            raise forms.ValidationError("Salary must be positive")
        return data

    def save(self, commit=True):
        if getattr(self, "instance", None) is None:
            raise ValueError("User is not set")
        if getattr(self.instance, "resume", None) is None:
            resume = Resume()
        else:
            resume = self.instance.resume
        resume.title = self.cleaned_data["title"]
        resume.salary = self.cleaned_data["salary"]
        resume.phone_number = (
            self.cleaned_data["phone_number"] or self.instance.phone_number
        )
        resume.experience = self.cleaned_data["experience"]
        resume.education = ""
        resume.achievements = self.cleaned_data["achievements"]
        resume.hobbies = self.cleaned_data["hobbies"]
        resume.additional_info = self.cleaned_data["additional_info"]
        resume.author = self.instance
        resume.save()

        resume.skills.set(self.cleaned_data["skills"])
        resume.save()
        return resume
