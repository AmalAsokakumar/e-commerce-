# Generated by Django 4.1.1 on 2022-10-04 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0011_alter_order_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, default="04-10-2022"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="orderproduct",
            name="updated_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]