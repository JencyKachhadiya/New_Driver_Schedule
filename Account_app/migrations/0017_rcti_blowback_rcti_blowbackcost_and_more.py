# Generated by Django 4.2.1 on 2023-12-27 11:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0016_pasttriperror_clientname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rcti',
            name='blowBack',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rcti',
            name='blowBackCost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rcti',
            name='blowBackGSTPayable',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rcti',
            name='blowBackTotal',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rcti',
            name='blowBackTotalExGST',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rcti',
            name='callOut',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rcti',
            name='callOutCost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rcti',
            name='callOutGSTPayable',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rcti',
            name='callOutTotal',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rcti',
            name='callOutTotalExGST',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rcti',
            name='surcharge_fixed_weekday',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rcti',
            name='surcharge_fixed_weekdayCost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rcti',
            name='surcharge_fixed_weekdayGSTPayable',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rcti',
            name='surcharge_fixed_weekdayTotal',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rcti',
            name='surcharge_fixed_weekdayTotalExGST',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rcti',
            name='surcharge_fixed_weekend',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rcti',
            name='surcharge_fixed_weekendCost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rcti',
            name='surcharge_fixed_weekendGSTPayable',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rcti',
            name='surcharge_fixed_weekendTotal',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rcti',
            name='surcharge_fixed_weekendTotalExGST',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2023, 12, 27, 11, 41, 30, 907132, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='rcti',
            name='waitingTimeInMinutes',
            field=models.FloatField(default=0),
        ),
    ]
