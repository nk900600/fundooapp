# Generated by Django 2.2.5 on 2019-10-12 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0005_notes_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='label',
            field=models.ManyToManyField(blank=True, related_name='label', to='note.Label'),
        ),
    ]