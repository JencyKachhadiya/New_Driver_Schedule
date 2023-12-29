# Generated by Django 4.2.1 on 2023-12-09 16:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0002_location_address_location_lat_location_long_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2023, 12, 9, 16, 22, 56, 157293, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterUniqueTogether(
            name='baseplant',
            unique_together={('lat', 'long')},
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together={('lat', 'long')},
        ),
    ]