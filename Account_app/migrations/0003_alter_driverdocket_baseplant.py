# Generated by Django 4.2.2 on 2023-10-13 05:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0002_alter_driverdocket_baseplant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverdocket',
            name='basePlant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Account_app.baseplant'),
        ),
    ]
