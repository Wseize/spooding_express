# Generated by Django 5.0.6 on 2024-07-08 14:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0005_alter_item_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliment',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='delivery.store'),
        ),
    ]
