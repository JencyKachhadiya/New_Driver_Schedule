# Generated by Django 4.2.2 on 2023-10-13 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0003_alter_driverdocket_baseplant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverdocket',
            name='basePlant',
            field=models.CharField(choices=[('select', 'SELECT'), ('Root', 'ROOT')], default='select', max_length=31),
        ),
    ]
