# Generated by Django 4.1.1 on 2022-10-09 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0017_order_offer_status"),
    ]

    operations = [
        migrations.DeleteModel(
            name="RazorOrder",
        ),
        migrations.AlterField(
            model_name="payment",
            name="status",
            field=models.CharField(default="Pending", max_length=100),
        ),
    ]