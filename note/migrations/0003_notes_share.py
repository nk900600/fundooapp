# Generated by Django 2.2.6 on 2019-10-06 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0002_auto_20191005_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='share',
            field=models.URLField(default='https://twitter.com/intent/tweet?source=webclient&text=<django.db.models.fields.CharField>'),
        ),
    ]