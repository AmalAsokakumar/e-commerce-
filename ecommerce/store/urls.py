from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

# main pages
from .views import home, contact, about

# category views
from .views import (
    add_category,
    upload_pic,
    view_category,
    edit_category,
    delete_category,
)

# brand views
from .views import add_brand, upload_pic_, view_brand, delete_brand, edit_brand

# product views
from .views import (
    add_product,
    upload_pic_pro,
    view_product,
    delete_product,
    edit_product,
)

# store view
from .views import store, product_detail, search

# cart
from .views import cart, add_cart, remove_cart, remove_cart_item

# checkout
from .views import checkout

# coupon
from .views import apply_coupon

urlpatterns = [
    # basic views
    path("", home, name="user_home"),
    path("contact/", contact, name="user_contact"),
    path("about/", about, name="user_about"),
    # category
    path("add/category/", add_category, name="add_category"),
    path("success/", upload_pic, name="category_success"),
    path("category/", view_category, name="category_view"),
    path("edit-category/<int:id>/", edit_category, name="edit_category"),
    path("delete-category/<int:id>/", delete_category, name="delete_category"),
    # brand
    path("add/brand/", add_brand, name="add_brand"),
    path("success/", upload_pic_, name="brand_success"),
    path("brand/", view_brand, name="brand_view"),
    path("edit-brand/<int:id>/", edit_brand, name="edit_brand"),
    path("delete-brand/<int:id>/", delete_brand, name="delete_brand"),
    #  product
    path("add/product/", add_product, name="add_product"),
    path("success/", upload_pic_pro, name="product_success"),
    path("product", view_product, name="product_view"),
    path("edit-product/<int:id>/", edit_product, name="edit_product"),
    path("delete-product/<int:id>/", delete_product, name="delete_product"),
    # store-views
    path("store/", store, name="store"),
    path("category/<slug:category_slug>/", store, name="products_by_category"),
    path(
        "category/<slug:category_slug>/<slug:product_slug>/",
        product_detail,
        name="product_detail",
    ),
    path("search/", search, name="search"),
    # cart
    path("cart/", cart, name="view_cart"),
    path("add-cart/<int:product_id>/", add_cart, name="add_cart"),
    path(
        "remove-cart/<int:product_id>/<int:cart_item_id>",
        remove_cart,
        name="remove_cart",
    ),
    path(
        "remove-cart-item/<int:product_id>/<int:cart_item_id>",
        remove_cart_item,
        name="remove_cart_item",
    ),
    # coupon
    path("cart/apply-coupon", apply_coupon, name="apply_coupon"),
    # special access needed
    path("checkout/", checkout, name="checkout"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
