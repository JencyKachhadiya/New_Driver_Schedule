# Generated by Django 4.2.2 on 2024-01-16 09:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0054_reconciliationreport_driverblowback_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2024, 1, 16, 9, 7, 42, 932647, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]