# Generated by Django 4.1.4 on 2023-04-24 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_disease_stage_alter_patient_mobile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='doctor',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.doctor'),
        ),
    ]
