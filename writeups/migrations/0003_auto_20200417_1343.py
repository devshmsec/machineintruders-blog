# Generated by Django 3.0.5 on 2020-04-17 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writeups', '0002_auto_20200417_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(default='default.jpg', upload_to='thumbnails/'),
        ),
    ]