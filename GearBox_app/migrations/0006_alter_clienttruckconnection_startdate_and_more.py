# Generated by Django 4.2.1 on 2023-12-27 11:41

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GearBox_app', '0005_alter_clienttruckconnection_startdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clienttruckconnection',
            name='startDate',
            field=models.DateField(default=datetime.datetime(2023, 12, 27, 11, 41, 20, 965842, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='costparameters',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2033, 12, 24, 11, 41, 20, 957878, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='costparameters',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 27, 11, 41, 20, 957878, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='grace',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2033, 12, 24, 11, 41, 20, 962855, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='grace',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 27, 11, 41, 20, 962855, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='onlease',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2033, 12, 24, 11, 41, 20, 963849, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='onlease',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 27, 11, 41, 20, 963849, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='thresholddayshift',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2033, 12, 24, 11, 41, 20, 960860, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='thresholddayshift',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 27, 11, 41, 20, 960860, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='thresholdnightshift',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2033, 12, 24, 11, 41, 20, 961855, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='thresholdnightshift',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 27, 11, 41, 20, 961855, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='RateCardSurchargeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surchargeValue', models.FloatField(default=0)),
                ('start_date', models.DateField(default=datetime.datetime(2023, 12, 27, 11, 41, 20, 959858, tzinfo=datetime.timezone.utc))),
                ('end_date', models.DateField(blank=True, default=datetime.datetime(2033, 12, 24, 11, 41, 20, 959858, tzinfo=datetime.timezone.utc), null=True)),
                ('rate_card_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GearBox_app.ratecard')),
                ('surcharge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GearBox_app.surcharge')),
            ],
        ),
    ]
