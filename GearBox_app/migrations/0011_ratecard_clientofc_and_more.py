# Generated by Django 5.0.1 on 2024-02-12 07:52

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GearBox_app', '0010_alter_clienttruckconnection_startdate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratecard',
            name='clientOfc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='GearBox_app.clientoffice'),
        ),
        migrations.AlterField(
            model_name='clienttruckconnection',
            name='startDate',
            field=models.DateField(default=datetime.datetime(2024, 2, 12, 7, 52, 0, 537346, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='costparameters',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 9, 7, 52, 0, 521719, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='costparameters',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 12, 7, 52, 0, 521719, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='grace',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 9, 7, 52, 0, 537346, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='grace',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 12, 7, 52, 0, 537346, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='onlease',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 9, 7, 52, 0, 537346, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='onlease',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 12, 7, 52, 0, 537346, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ratecard',
            name='clientName',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='GearBox_app.client'),
        ),
        migrations.AlterField(
            model_name='ratecardsurchargevalue',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 9, 7, 52, 0, 521719, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='ratecardsurchargevalue',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 12, 7, 52, 0, 521719, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='thresholddayshift',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 9, 7, 52, 0, 521719, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='thresholddayshift',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 12, 7, 52, 0, 521719, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='thresholdnightshift',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 9, 7, 52, 0, 521719, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='thresholdnightshift',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 12, 7, 52, 0, 521719, tzinfo=datetime.timezone.utc)),
        ),
    ]
