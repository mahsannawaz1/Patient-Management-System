# Generated by Django 4.1.4 on 2023-04-24 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_patient_doctor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disease',
            name='duration',
        ),
    ]