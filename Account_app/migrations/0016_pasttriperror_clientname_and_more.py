# Generated by Django 4.2.1 on 2023-12-26 04:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0015_alter_driverdocket_shiftdate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pasttriperror',
            name='clientName',
            field=models.CharField(blank=True, default=None, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2023, 12, 26, 4, 14, 45, 586011, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
