# Generated by Django 2.2 on 2019-07-07 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judger', '0026_auto_20190707_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='memory_used',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='code',
            name='time_used',
            field=models.IntegerField(default=0),
        ),
    ]
