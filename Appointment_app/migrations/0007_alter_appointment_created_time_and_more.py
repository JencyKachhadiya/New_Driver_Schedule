# Generated by Django 4.2.2 on 2023-12-26 07:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment_app', '0006_prestart_curdate_alter_appointment_created_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='Created_time',
            field=models.TimeField(default=datetime.datetime(2023, 12, 26, 7, 9, 22, 842717, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='End_Date_Time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 26, 7, 9, 22, 842717, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='Start_Date_Time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 26, 7, 9, 22, 842717, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='report_to_origin',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 26, 7, 9, 22, 842717, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='prestart',
            name='curDate',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 26, 7, 9, 22, 843747, tzinfo=datetime.timezone.utc)),
        ),
    ]
