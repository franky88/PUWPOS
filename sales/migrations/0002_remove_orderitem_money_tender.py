# Generated by Django 4.1.5 on 2023-08-21 01:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='money_tender',
        ),
    ]
