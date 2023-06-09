# Generated by Django 4.1.4 on 2023-02-20 16:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0009_alter_prescription_patient"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appointment",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Cancelled", "Cancelled"),
                    ("Accepted", "Accepted"),
                    ("Completed", "Completed"),
                ],
                default="Pending",
                max_length=255,
            ),
        ),
    ]
