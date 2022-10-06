from .models import Category
from .models import Brand
from .models import Product
from .models import Coupon
from .models import UsedCoupon
from .models import Variation
from .models import Offers
from django.forms import ModelForm, TextInput, ClearableFileInput
from django import forms


# category
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ["category_name", "description", "cat_image", "offer_status"]
        widgets = {
            "cat_image": ClearableFileInput(
                attrs={"class": "form-control-file", "style": "width:80%"}
            )
        }

    def __init__(
        self, *arg, **kwargs
    ):  # using a constructor i am applying style to each field of the above form (
        # applying class
        # form-control to every field it can also be done in mata class just like on the above class i have created
        # password field and applied a widget for it to apply form control to it )
        super(CategoryForm, self).__init__(*arg, **kwargs)
        self.fields["category_name"].widget.attrs["placeholder"] = "Enter Category Name"
        self.fields["description"].widget.attrs["placeholder"] = "Description"
        self.fields["offer_status"].widget.attrs["placeholder"] = "offer_status"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


# brand
class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = ["brand_name", "description", "brand_image", "offer_status"]
        widgets = {
            "brand_image": ClearableFileInput(
                attrs={"class": "form-control-file", "style": "width:80%"}
            )
        }

    def __init__(
        self, *arg, **kwargs
    ):  # using a constructor am applying style to each field of the above form (
        # applying
        # class form-control to every field it can also be done in mata class just like on the above class i have
        # created password field and applied a widget for it to apply form control to it )
        super(BrandForm, self).__init__(*arg, **kwargs)
        self.fields["brand_name"].widget.attrs["placeholder"] = "Enter Brand Name"
        self.fields["description"].widget.attrs["placeholder"] = "Description"
        self.fields["offer_status"].widget.attrs["placeholder"] = "offer_status"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


# product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            "product_name",
            "slug",
            "description",
            "price",
            "images",
            "stock",
            "is_available",
            "offer_status",
            "category",
            "brand",
        ]
        widgets = {
            "images": ClearableFileInput(
                attrs={"class": "form-control-file", "style": "width:80%"}
            )
        }


class CouponForm(ModelForm):
    class Meta:
        model = Coupon
        fields = ["coupon_name", "coupon_code", "amount"]


class UsedCouponForm(ModelForm):
    class Meta:
        model = UsedCoupon
        fields = ["coupon", "user"]


class VariationForm(ModelForm):
    class Meta:
        model = Variation
        fields = [
            "product",
            "variation_category",
            "variation_value",
            "is_active",
        ]


class OffersForm(ModelForm):
    category_offer = forms.IntegerField()
    brand_offer = forms.IntegerField()
    product_offer = forms.IntegerField()

    class Meta:
        model = Offers
        fields = [
            "category",
            "category_offer",
            "brand",
            "brand_offer",
            "product",
            "product_offer",
        ]
