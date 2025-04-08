# Generated by Django 5.1.6 on 2025-04-08 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_questionpaper_blockchain_hash_questionpaper_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
                ('data', models.JSONField()),
                ('previous_hash', models.CharField(max_length=256)),
                ('current_hash', models.CharField(max_length=256)),
            ],
        ),
    ]
