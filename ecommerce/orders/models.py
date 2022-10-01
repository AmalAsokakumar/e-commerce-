from django.db import models
from accounts.models import Account
from store.models import Product
from store.models import Variation


# SET_DEFAULT: Set the default value. SQL equivalent: SET DEFAULT.
# SET(...): Set a given value. This one is not part of the SQL standard and is entirely handled by Django.
# RESTRICT: (introduced in Django 3.1) Similar behavior as PROTECT that matches SQL's RESTRICT more accurately.
# PROTECT: Forbid the deletion of the referenced object. To delete it you will have to delete all objects that
# reference it manually. SQL equivalent: RESTRICT. Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


# SET_NULL: Set the reference to NULL (requires the field to be nullable). For instance, when you delete a User,
# you might want to keep the comments he posted on blog posts, but say it was posted by an anonymous (or deleted)
# user. SQL equivalent: SET NULL.


class Order(models.Model):  # even if the user gets deleted we want to keep the data.
    STATUS = (
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Completed", "Completed"),
        ("Canceled", "Canceled"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True
    )
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    pincode = models.CharField(max_length=50, blank=True)
    landmark = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default="New")
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #
    #     # auto_now - updates the value of field to current time and date every time the Model. save() is called.
    #     # auto_now_add - updates the value with the time and date of creation of record

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def full_address(self):
        return f"{self.address_line_1} {self.address_line_2} "

    def __str__(self):
        return self.first_name

    # CASCADE: When the referenced object is deleted, also delete the objects that have references to it (when you
    # remove a blog post for instance, you might want to delete comments as well). SQL equivalent: CASCADE.


class OrderProduct(
    models.Model
):  # we don't need to keep the Ordered products if the order gets deleted
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
