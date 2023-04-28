# Generated by Django 4.1.4 on 2023-04-28 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_alter_prescription_medicines'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, default='-', max_length=100, null=True)),
                ('state', models.CharField(blank=True, default='-', max_length=100, null=True)),
                ('country', models.CharField(blank=True, default='-', max_length=100, null=True)),
                ('house_address', models.CharField(blank=True, default='-', max_length=500, null=True)),
                ('patient', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.patient')),
            ],
        ),
    ]
