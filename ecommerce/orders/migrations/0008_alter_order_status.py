# Generated by Django 4.1.1 on 2022-10-02 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0007_remove_orderproduct_variations_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("New", "New"),
                    ("Accepted", "Accepted"),
                    ("Completed", "Completed"),
                    ("Canceled", "Canceled"),
                    ("Shipped", "Shipped"),
                    ("Delivered", "Delivered"),
                    ("Cancelled", "Cancelled"),
                ],
                default="New",
                max_length=10,
            ),
        ),
    ]