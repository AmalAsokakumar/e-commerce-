# Generated by Django 4.1.1 on 2022-09-26 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_order_landmark_order_pincode_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='color',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='size',
        ),
    ]