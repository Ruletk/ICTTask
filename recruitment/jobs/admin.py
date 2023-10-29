from django import forms
from django.contrib import admin
from jobs.models import Company
from jobs.models import Possibility
from jobs.models import Skill
from jobs.models import Vacancy
from jobs.models.miscs import ColorField


# Register your models here.
@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    class Meta:
        model = Vacancy
        fields = ("title", "description", "salary", "company", "published_at")

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(VacancyAdmin, self).get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

    class Meta:
        model = Skill
        fields = ("name", "vacancies")


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

    class Meta:
        model = Company
        fields = ("name", "location", "logo", "description", "employee_count", "owner")


@admin.register(Possibility)
class PossibilityAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

    formfield_overrides = {
        ColorField: {"widget": forms.TextInput(attrs={"type": "color"})},
    }

    class Meta:
        model = Possibility
        fields = ("name", "vacancies", "background_color", "text_color")
