# Generated by Django 5.0.1 on 2024-02-12 10:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentstop',
            name='arrivalTime',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointmentstop',
            name='duration',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='appointmentstop',
            name='noted',
            field=models.CharField(default='', max_length=2048, null=True),
        ),
        migrations.AddField(
            model_name='appointmentstop',
            name='stopType',
            field=models.CharField(choices=[('Stop', 'Stop'), ('Pickup', 'Pickup'), ('Dropoff', 'Dropoff')], default='Stop', max_length=100),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='createdTime',
            field=models.TimeField(blank=True, default=datetime.datetime(2024, 2, 12, 10, 29, 25, 223935, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='prestartquestion',
            name='questionType',
            field=models.CharField(choices=[('Driver related', 'Driver related'), ('Vehicle related', 'Vehicle related'), ('Other', 'Other')], max_length=20),
        ),
    ]
