# Generated by Django 2.2.5 on 2019-10-01 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0003_auto_20191001_0539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='label',
            field=models.ManyToManyField(blank=True, related_name='label', to='note.Lable'),
        ),
    ]
