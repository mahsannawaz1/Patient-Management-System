# Generated by Django 4.1.4 on 2023-04-25 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_alter_admin_user_alter_doctor_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nurse',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.doctor'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patient', to='accounts.doctor'),
        ),
    ]
