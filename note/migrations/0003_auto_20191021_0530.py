# Generated by Django 2.2.6 on 2019-10-21 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0002_auto_20191017_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='image',
            field=models.FileField(blank=True, max_length=500, null=True, upload_to='image'),
        ),
    ]
