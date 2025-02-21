from django import forms
from django.contrib import admin
from .models import SiteOptions, Partners


class SiteOptionsForm(forms.ModelForm):
    class Meta:
        model = SiteOptions
        fields = "__all__"
        widgets = {
            "custom_css": forms.Textarea(attrs={"rows": 50, "cols": 100}),
        }


@admin.register(SiteOptions)
class SiteOptionsAdmin(admin.ModelAdmin):
    form = SiteOptionsForm
    list_display = ["sponsor_name", "sponsor_url", "sponsor_logo"]


@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ["name", "url"]
