# Generated by Django 5.1.4 on 2025-01-02 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
    ]
