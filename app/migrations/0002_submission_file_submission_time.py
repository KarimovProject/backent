# Generated by Django 5.1.1 on 2024-10-16 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='file',
            field=models.FileField(default='12.02.2003', upload_to='files/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default="2003-07-12 10:10"),
            preserve_default=False,
        ),
    ]