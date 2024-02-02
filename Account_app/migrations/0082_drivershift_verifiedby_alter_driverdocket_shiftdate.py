# Generated by Django 5.0.1 on 2024-01-31 10:04

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0081_rctierrors_exceptiontext_rctierrors_truckno_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='drivershift',
            name='verifiedBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2024, 1, 31, 10, 4, 28, 339995, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
