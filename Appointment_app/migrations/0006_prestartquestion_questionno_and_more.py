# Generated by Django 5.0.1 on 2024-03-04 03:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment_app', '0005_alter_appointment_createdtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestartquestion',
            name='questionNo',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='createdTime',
            field=models.TimeField(blank=True, default=datetime.datetime(2024, 3, 4, 3, 59, 6, 317847, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='prestartquestion',
            name='questionType',
            field=models.CharField(choices=[('Other', 'Other'), ('Driver related', 'Driver related'), ('Vehicle related', 'Vehicle related')], max_length=20),
        ),
    ]