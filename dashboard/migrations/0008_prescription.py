# Generated by Django 4.1.4 on 2023-02-18 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_alter_appointment_patient'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('medicine_type', models.CharField(max_length=255, null=True)),
                ('duration', models.CharField(max_length=255, null=True)),
                ('usage', models.CharField(max_length=255, null=True)),
                ('comment', models.TextField(blank=True, max_length=255, null=True)),
                ('patient', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.patient')),
            ],
        ),
    ]
