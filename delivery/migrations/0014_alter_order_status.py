# Generated by Django 5.0.6 on 2024-07-22 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0013_store_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Received', 'Received'), ('In Progress', 'In Progress'), ('In Transit', 'In Transit'), ('Complete', 'Complete'), ('Cancelled', 'Cancelled'), ('Confirmed', 'Confirmed'), ('Returned', 'Returned')], default='Received', max_length=20),
        ),
    ]
