# Generated by Django 2.2.6 on 2019-11-19 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SocialLogin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(max_length=500)),
                ('provider', models.CharField(max_length=500, verbose_name='service provider')),
                ('username', models.CharField(max_length=500)),
                ('full_name', models.CharField(max_length=500)),
                ('EXTRA_PARAMS', models.TextField(max_length=1000, verbose_name='extra params')),
            ],
        ),
    ]