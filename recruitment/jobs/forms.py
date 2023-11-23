from datetime import datetime

from django import forms
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
        print(value)
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


class CreateResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = (
            "title",
            "salary",
            "skills",
            "phone_number",
            "experience",
            "education",
            "achievements",
            "hobbies",
            "additional_info",
        )
