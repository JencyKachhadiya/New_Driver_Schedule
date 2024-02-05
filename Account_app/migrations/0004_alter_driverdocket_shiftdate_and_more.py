# Generated by Django 4.2.2 on 2024-02-04 13:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0003_escalationdocket_callout_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2024, 2, 4, 13, 10, 28, 166502, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='escalation',
            name='escalationAmount',
            field=models.FloatField(default=0),
        ),
    ]
