# Generated by Django 5.1.3 on 2024-11-08 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0010_remove_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_brand',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
