# Generated by Django 2.0.2 on 2018-06-15 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clockin', '0018_bill_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='work_intervals',
            field=models.ManyToManyField(default=[], to='clockin.IntervalWork'),
        ),
    ]
