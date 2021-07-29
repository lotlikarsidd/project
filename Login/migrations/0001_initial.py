# Generated by Django 3.1.7 on 2021-07-06 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('username', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('timestamp_login', models.DateTimeField(blank=True, null=True)),
                ('timestamp_logout', models.DateTimeField(blank=True, null=True)),
                ('iscustomer', models.BooleanField(default=False)),
                ('isowner', models.BooleanField(default=False)),
                ('total_usage', models.DateTimeField(blank=True, null=True)),
                ('oname', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('oid', models.AutoField(primary_key=True, serialize=False)),
                ('oname', models.CharField(max_length=100)),
                ('opic', models.FileField(blank=True, null=True, upload_to='')),
                ('ophone_no', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('oaddress', models.CharField(blank=True, max_length=500, null=True)),
                ('oemail', models.EmailField(max_length=100)),
                ('orating', models.FloatField(blank=True, null=True)),
                ('odob', models.DateField(blank=True, null=True)),
                ('Lattitude', models.FloatField(blank=True, null=True)),
                ('Longitude', models.FloatField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=500, null=True)),
                ('active', models.BooleanField(default=False)),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Login.login')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('cid', models.AutoField(primary_key=True, serialize=False)),
                ('cname', models.CharField(max_length=100)),
                ('cpic', models.FileField(blank=True, null=True, upload_to='')),
                ('cphone_no', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('caddress', models.CharField(blank=True, max_length=100, null=True)),
                ('cemail', models.EmailField(max_length=100)),
                ('crating', models.FloatField(blank=True, null=True)),
                ('cdob', models.DateField(blank=True, null=True)),
                ('Lattitude', models.FloatField(blank=True, null=True)),
                ('Longitude', models.FloatField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=500, null=True)),
                ('active', models.BooleanField(default=False)),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Login.login')),
            ],
        ),
    ]
