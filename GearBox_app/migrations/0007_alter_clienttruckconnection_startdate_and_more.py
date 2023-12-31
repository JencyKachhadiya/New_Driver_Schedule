# Generated by Django 4.2.1 on 2023-12-27 13:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GearBox_app', '0006_alter_clienttruckconnection_startdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clienttruckconnection',
            name='startDate',
            field=models.DateField(default=datetime.datetime(2023, 12, 27, 13, 36, 37, 312179, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='costparameters',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2033, 12, 24, 13, 36, 37, 308153, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='costparameters',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 27, 13, 36, 37, 308153, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='grace',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2033, 12, 24, 13, 36, 37, 310189, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='grace',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 27, 13, 36, 37, 310189, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='onlease',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2033, 12, 24, 13, 36, 37, 311183, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='onlease',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 27, 13, 36, 37, 311183, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ratecardsurchargevalue',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2033, 12, 24, 13, 36, 37, 309149, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='ratecardsurchargevalue',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 27, 13, 36, 37, 309149, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='thresholddayshift',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2033, 12, 24, 13, 36, 37, 309149, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='thresholddayshift',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 27, 13, 36, 37, 309149, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='thresholdnightshift',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2033, 12, 24, 13, 36, 37, 310189, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='thresholdnightshift',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 27, 13, 36, 37, 310189, tzinfo=datetime.timezone.utc)),
        ),
    ]
