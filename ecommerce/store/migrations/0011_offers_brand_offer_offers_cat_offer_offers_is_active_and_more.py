# Generated by Django 4.1.1 on 2022-10-05 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0010_rename_offer_offers"),
    ]

    operations = [
        migrations.AddField(
            model_name="offers",
            name="brand_offer",
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name="offers",
            name="cat_offer",
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name="offers",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="offers",
            name="product_offer",
            field=models.IntegerField(default=0, null=True),
        ),
    ]
