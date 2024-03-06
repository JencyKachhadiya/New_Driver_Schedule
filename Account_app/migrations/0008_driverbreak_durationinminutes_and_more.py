# Generated by Django 5.0.1 on 2024-03-06 08:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0007_drivershift_locationimg_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverbreak',
            name='durationInMinutes',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2024, 3, 6, 8, 59, 47, 327020, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
