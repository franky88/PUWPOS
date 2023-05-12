# Generated by Django 4.1.5 on 2023-05-12 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0021_rename_category_productcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('basetime_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sales.basetime')),
                ('image_name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product-image/%Y/%m/%d')),
            ],
            bases=('sales.basetime',),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ManyToManyField(blank=True, null=True, to='sales.productimage'),
        ),
    ]
