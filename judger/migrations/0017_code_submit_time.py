# Generated by Django 2.1.5 on 2019-03-14 15:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('judger', '0016_auto_20190312_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='submit_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]