# Generated by Django 2.1.5 on 2019-07-12 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judger', '0027_auto_20190707_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='contestant',
            field=models.ManyToManyField(null=True, to='judger.User'),
        ),
    ]