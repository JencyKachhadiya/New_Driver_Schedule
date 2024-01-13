# Generated by Django 4.2.2 on 2024-01-13 09:01

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment_app', '0009_alter_appointment_created_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prestart',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='prestart',
            name='curDate',
        ),
        migrations.RemoveField(
            model_name='prestart',
            name='driver',
        ),
        migrations.RemoveField(
            model_name='prestart',
            name='fitForWork',
        ),
        migrations.RemoveField(
            model_name='prestart',
            name='vehiclePaper',
        ),
        migrations.RemoveField(
            model_name='prestart',
            name='vehicleStatus',
        ),
        migrations.AddField(
            model_name='prestart',
            name='createdDate',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='prestart',
            name='preStartName',
            field=models.CharField(default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='Created_time',
            field=models.TimeField(default=datetime.datetime(2024, 1, 13, 9, 1, 38, 184583, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='End_Date_Time',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 13, 9, 1, 38, 184583, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='Start_Date_Time',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 13, 9, 1, 38, 184583, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='report_to_origin',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 13, 9, 1, 38, 184583, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='PreStartQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questionText', models.CharField(default='', max_length=1024, null=True)),
                ('questionType', models.CharField(choices=[('Other', 'Other'), ('Driver related', 'Driver related'), ('Vehicle related', 'Vehicle related')], max_length=20)),
                ('optionTxt1', models.CharField(default='', max_length=30, null=True)),
                ('wantFile1', models.BooleanField(default=False)),
                ('optionFile1', models.FileField(blank=True, null=True, upload_to='')),
                ('optionComment1', models.CharField(default='', max_length=1024, null=True)),
                ('optionTxt2', models.CharField(blank=True, max_length=30, null=True)),
                ('wantFile2', models.BooleanField(default=False)),
                ('optionFile2', models.FileField(blank=True, null=True, upload_to='')),
                ('optionComment2', models.CharField(default='', max_length=1024, null=True)),
                ('optionTxt3', models.CharField(blank=True, max_length=30, null=True)),
                ('wantFile3', models.BooleanField(default=False)),
                ('optionFile3', models.FileField(blank=True, null=True, upload_to='')),
                ('optionComment3', models.CharField(default='', max_length=1024, null=True)),
                ('optionTxt4', models.CharField(blank=True, max_length=30, null=True)),
                ('wantFile4', models.BooleanField(default=False)),
                ('optionFile4', models.FileField(blank=True, null=True, upload_to='')),
                ('optionComment4', models.CharField(default='', max_length=1024, null=True)),
                ('preStartId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Appointment_app.prestart')),
            ],
        ),
    ]