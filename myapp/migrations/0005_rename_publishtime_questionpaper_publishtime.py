# Generated by Django 5.1.6 on 2025-04-12 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_questionpaper_publishdate_questionpaper_publishtime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questionpaper',
            old_name='publishTIme',
            new_name='publishTime',
        ),
    ]
