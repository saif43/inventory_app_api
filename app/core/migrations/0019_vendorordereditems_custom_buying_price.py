# Generated by Django 2.2.16 on 2020-10-17 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_product_avg_buying_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorordereditems',
            name='custom_buying_price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]