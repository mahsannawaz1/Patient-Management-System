# Generated by Django 4.1.4 on 2023-04-24 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_newuser_age'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_phone', models.PositiveSmallIntegerField(max_length=12)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.doctor')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='patient', to='accounts.newuser')),
            ],
        ),
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('duration', models.CharField(max_length=100)),
                ('stage', models.PositiveSmallIntegerField(max_length=5)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.patient')),
            ],
        ),
    ]
