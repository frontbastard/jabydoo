from django import forms
from django.contrib import admin
from django_ace import AceWidget

from .models import SiteOptions, Partners


class SiteOptionsForm(forms.ModelForm):
    class Meta:
        model = SiteOptions
        fields = "__all__"
        widgets = {
            "custom_css": AceWidget(
                mode="css",
                width="100%",
                height="500px",
                showprintmargin=False,
            ),
        }


@admin.register(SiteOptions)
class SiteOptionsAdmin(admin.ModelAdmin):
    form = SiteOptionsForm


@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ["name", "url"]
