# Register your models here.
from django.contrib import admin

# category
from .models import Category

# brand
from .models import Brand

# store and variations
from .models import Product, Variation

# cart
from django.contrib.auth.admin import UserAdmin
from .models import Cart, CartItem

# coupon
from .models import Coupon
from .models import UsedCoupon
from .models import Offers


# category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "slug", "cat_image")
    prepopulated_fields = {"slug": ("category_name",)}


# brand
class BrandAdmin(admin.ModelAdmin):
    list_display = ("brand_name", "slug", "brand_image")
    prepopulated_fields = {"slug": ("brand_name",)}


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "product_name",
        "price",
        "stock",
        "category",
        "modified_date",
        "is_available",
    )
    prepopulated_fields = {"slug": ("product_name",)}


class VariationAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "variation_category",
        "variation_value",
        "is_active",
        "created_date",
    )
    list_editable = ("is_active",)

    list_filter = ("product", "variation_category", "variation_value", "is_active")


class CartAdmin(admin.ModelAdmin):
    list_display = ("cart_id", "date_added")
    list_display_links = ()
    readonly_fields = ("cart_id", "date_added")
    ordering = ("-date_added",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity", "is_active")
    list_display_links = ("product", "cart")
    readonly_fields = ("cart_id",)
    ordering = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


#  Coupon
class CouponAdmin(admin.ModelAdmin):
    list_display = ("coupon_name", "coupon_code", "is_active")


class UsedCouponAdmin(admin.ModelAdmin):
    list_display = ("coupon", "user")


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)

admin.site.register(Variation, VariationAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(UsedCoupon, UsedCouponAdmin)
admin.site.register(Offers)
