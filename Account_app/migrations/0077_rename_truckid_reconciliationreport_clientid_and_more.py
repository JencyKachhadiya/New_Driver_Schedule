# Generated by Django 4.2.1 on 2024-01-21 09:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0076_alter_driverdocket_shiftdate_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reconciliationreport',
            old_name='truckId',
            new_name='clientId',
        ),
        migrations.RemoveField(
            model_name='reconciliationreport',
            name='clientName',
        ),
        migrations.AddField(
            model_name='reconciliationreport',
            name='truckConnectionId',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2024, 1, 21, 9, 54, 9, 87818, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
