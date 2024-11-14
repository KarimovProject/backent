# Generated by Django 5.1.2 on 2024-11-14 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_submission_file_submission_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='mname',
            field=models.CharField(default='nomalum', max_length=100),
        ),
        migrations.AddField(
            model_name='submission',
            name='reviewed',
            field=models.BooleanField(default=False),
        ),
    ]
