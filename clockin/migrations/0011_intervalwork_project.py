# Generated by Django 2.0.2 on 2018-03-25 03:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_project'),
        ('clockin', '0010_remove_intervalwork_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='intervalwork',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='invoice.Project'),
            preserve_default=False,
        ),
    ]
