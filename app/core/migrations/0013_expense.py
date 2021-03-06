# Generated by Django 2.2.16 on 2020-10-10 15:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20201010_1026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=0, editable=False)),
                ('created_timestamp', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Shop')),
            ],
        ),
    ]
