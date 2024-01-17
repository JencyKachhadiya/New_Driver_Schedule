# Generated by Django 4.2.1 on 2024-01-16 14:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0056_alter_driverdocket_shiftdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2024, 1, 16, 14, 4, 59, 406863, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='rcti',
            name='others',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='rcti',
            name='standByUnit',
            field=models.CharField(choices=[('minute', 'MINUTE'), ('slot', 'SLOT')], default='minute', max_length=20),
        ),
    ]
