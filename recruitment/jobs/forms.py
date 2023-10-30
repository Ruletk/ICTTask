from django import forms


class SearchJobForm(forms.Form):
    keyword = forms.CharField(max_length=255, required=False)
    location = forms.CharField(max_length=255, required=False)
    salary = forms.FloatField(required=False)
