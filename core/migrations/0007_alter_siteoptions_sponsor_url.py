# Generated by Django 5.1.5 on 2025-02-18 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_siteoptions_site_type_alter_siteoptions_ai_model"),
    ]

    operations = [
        migrations.AlterField(
            model_name="siteoptions",
            name="sponsor_url",
            field=models.URLField(help_text="Referral link to sponsor", max_length=255),
        ),
    ]
