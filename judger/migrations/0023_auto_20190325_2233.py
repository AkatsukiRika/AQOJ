# Generated by Django 2.1.5 on 2019-03-25 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judger', '0022_user_ac_count'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-ac_count'], 'verbose_name': 'OJ用户', 'verbose_name_plural': 'OJ用户'},
        ),
        migrations.AlterField(
            model_name='user',
            name='accepted',
            field=models.ManyToManyField(null=True, to='judger.Problem'),
        ),
    ]
