# Generated by Django 2.2.6 on 2019-10-12 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0002_auto_20191012_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='name',
            field=models.CharField(max_length=254, unique=True),
        ),
    ]