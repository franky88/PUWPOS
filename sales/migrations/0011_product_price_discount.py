# Generated by Django 4.1.5 on 2023-05-03 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0010_product_price_margin'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_discount',
            field=models.FloatField(default=0.2),
        ),
    ]
