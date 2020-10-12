# Generated by Django 2.2.16 on 2020-10-11 21:24

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_vendortrasnscation_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendortrasnscation',
            name='image',
        ),
        migrations.AddField(
            model_name='vendorordereditems',
            name='image',
            field=models.ImageField(null=True, upload_to=core.models.transaction_image_file_path),
        ),
    ]