# Generated by Django 4.1.4 on 2023-04-28 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='patient',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='address', to='accounts.patient'),
        ),
    ]
