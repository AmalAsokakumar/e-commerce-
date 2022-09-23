from django.db import models
from django.urls import reverse

import uuid


# things to learn from here
# what is slug and how to use it properly.
# details of metaclass


# Create your models here

# category .
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(
        unique=True)  # should be the url of the category, and it should be unique, this field should be auto
    # generated because we use SlugField for this slug, to properly use this feature we need to configure the
    # admin.py file
    description = models.TextField(max_length=255, blank=True)  # blank= True means this field is optional, which can
    # be empty.
    cat_image = models.ImageField(upload_to='photos/category/', blank=True)  # this should be the location where the
    # photos will be uploaded into.
    offer_status = models.BooleanField(default=False)

    # used to fix the typo error in admin page.
    class Meta:  # with the metaclass we are editing the category name and other things.
        #  db_table = 'category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'  # to fix the name which is give in the admin dashboard

    # with this function we can bring back the url of a particular category
    def get_url(self):
        return reverse('products_by_category', args=[
            self.slug])  # here we will mention the name of <slug:category_slug> in Stor urls.py file, we are also
        # passing slug in list as arguments

    # creating string way representation of the model ?
    def __str__(self):
        return self.category_name


# brand
class Brand(models.Model):
    brand_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)  # default=uuid.uuid1
    description = models.TextField(max_length=255, blank=True)
    brand_image = models.ImageField(upload_to='photos/brand/', blank=True)
    offer_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        # db_table = 'brand'

    def __str__(self):
        return self.brand_name


# from brand.models import brand
# Create your models here.

# for further reference
# 1  _ difference b/w  auto_add_now and auto_add.


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    offer_status = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # (model_name, what to do when we delete this
    # category) here the entire Field will be deleted when delete this particular field.
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])  # here we have 2 arguments product
        # slugs and categories slug. here self means this product and category is mentioned above and slug is from
        # category app ( we can access them because these fields are interconnected with : foreignkey . )   and
        # second slug is this products slug.

    def __str__(self):
        return self.product_name


class VariationManager(models.Manager):
    def color(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def size(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choice = (  # this is used to create a drop down variation list for the product.
    ('color', 'color'),
    ('size', 'size'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()  # only now will the two functions which are defined above will start working.

    # def __str__(self):
    #     self.variation_value
    def __unicode__(self):
        return self.variation_value


# cart
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


# wish list  have some bugs we can do that later
# class WishList(models.Model):
#     wish_list_id = models.CharField(max_length=250, blank=True)
#     date_added = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.wish_list_id

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # model (model name)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    # def __unicode__(self):
    #     return self.product

    def __str__(self):
        return self.product.product_name

# class WishListItems(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     wish_list = models.ForeignKey(WishList, on_delete=models.CASCADE)
#     is_active = True
#
#     def __str__(self):
#         return self.product.product_name


# class WishList:
#     wish_list_id = models.CharField(max_length=250, blank=True)
#     date_added = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.wish_list_id
