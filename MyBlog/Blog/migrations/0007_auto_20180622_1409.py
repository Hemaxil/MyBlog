# Generated by Django 2.0.6 on 2018-06-22 08:39

import Blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0006_auto_20180622_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to=Blog.models.upload_location, width_field='width_field'),
        ),
    ]