# Generated by Django 5.1.4 on 2025-01-03 09:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_order_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.product'),
        ),
    ]
