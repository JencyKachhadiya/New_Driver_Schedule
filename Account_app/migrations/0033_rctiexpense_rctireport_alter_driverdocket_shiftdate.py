# Generated by Django 4.2.1 on 2024-01-04 12:34

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0032_alter_driverdocket_shiftdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='rctiexpense',
            name='rctiReport',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Account_app.rctireport'),
        ),
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2024, 1, 4, 12, 34, 5, 787450, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
