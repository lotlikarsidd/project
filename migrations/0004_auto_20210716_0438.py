# Generated by Django 3.1.7 on 2021-07-15 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lend', '0003_auto_20210714_0158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bike',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='car',
            name='slug',
        ),
        migrations.AddField(
            model_name='bike',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='car',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
