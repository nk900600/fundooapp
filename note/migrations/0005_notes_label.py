# Generated by Django 2.2.6 on 2019-10-12 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0004_remove_notes_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='label',
            field=models.ManyToManyField(related_name='label', to='note.Label'),
        ),
    ]
