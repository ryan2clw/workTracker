# Generated by Django 2.0.2 on 2018-02-26 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clockin', '0003_intervalwork'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intervalwork',
            name='user',
        ),
        migrations.DeleteModel(
            name='IntervalWork',
        ),
    ]
