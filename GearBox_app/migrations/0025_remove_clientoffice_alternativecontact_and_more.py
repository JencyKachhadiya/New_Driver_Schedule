# Generated by Django 5.0.1 on 2024-02-28 13:49

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GearBox_app', '0024_remove_ratecard_clientofc_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientoffice',
            name='alternativeContact',
        ),
        migrations.RemoveField(
            model_name='clientoffice',
            name='personName',
        ),
        migrations.RemoveField(
            model_name='clientoffice',
            name='primaryContact',
        ),
        migrations.AlterField(
            model_name='clienttruckconnection',
            name='startDate',
            field=models.DateField(default=datetime.datetime(2024, 2, 28, 13, 49, 12, 323015, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='costparameters',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 25, 13, 49, 12, 310016, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='costparameters',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 28, 13, 49, 12, 310016, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='grace',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 25, 13, 49, 12, 313016, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='grace',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 28, 13, 49, 12, 313016, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='onlease',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 25, 13, 49, 12, 314015, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='onlease',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 28, 13, 49, 12, 314015, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ratecardsurchargevalue',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 25, 13, 49, 12, 311017, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='ratecardsurchargevalue',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 28, 13, 49, 12, 311017, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='thresholddayshift',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 25, 13, 49, 12, 312016, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='thresholddayshift',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 28, 13, 49, 12, 312016, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='thresholdnightshift',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 25, 13, 49, 12, 312016, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='thresholdnightshift',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 28, 13, 49, 12, 312016, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='ClientOfficeAdditionalInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personName', models.CharField(default='', max_length=100, null=True)),
                ('primaryContact', models.IntegerField(default=0, null=True)),
                ('alternativeContact', models.IntegerField(default=0, null=True)),
                ('email', models.CharField(default='', max_length=255, null=True)),
                ('clientOfficeId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='GearBox_app.clientoffice')),
            ],
        ),
    ]
