# Generated by Django 2.1.5 on 2019-03-12 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judger', '0015_code_postman'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='AC',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='code',
            name='CE',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='code',
            name='MLE',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='code',
            name='RE',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='code',
            name='TLE',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='code',
            name='WA',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='code',
            name='WJ',
            field=models.BooleanField(default=False),
        ),
    ]