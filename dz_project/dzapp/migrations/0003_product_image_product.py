# Generated by Django 4.2.5 on 2023-10-05 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dzapp', '0002_rename_order_id_order_buyer'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_product',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]