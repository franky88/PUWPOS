# Generated by Django 4.1.5 on 2023-05-09 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0018_alter_stocktransaction_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cost',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(default=0.0, verbose_name='SRP'),
        ),
    ]