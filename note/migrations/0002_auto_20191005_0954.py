# Generated by Django 2.2.6 on 2019-10-05 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='image',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to='image'),
        ),
    ]
