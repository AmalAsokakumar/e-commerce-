from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import (
    UserAdmin,
)  # this module is included to edit the lis which is shown on the admin page
from .models import Account, UserProfile
from django.utils.html import format_html


# #we need to delete the existing database ("db.sqlite3") to make migrations, because we dont want all those old data, which also included the super user and delete the migrations from category app along with it


class AccountAdmin(UserAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "username",
        "last_login",
        "date_joined",
        "is_active",
    )  # we need to follow some rules because we are using custom model
    list_display_links = ("email", "first_name", "last_name")
    readonly_fields = ("last_login", "date_joined")
    ordering = (
        "-date_joined",
    )  # '-' sign is used because we are showing this list in reversed(Descending order) order.

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html(
            '<img src="{}" width=30  style="border-radius:50%">'.format(
                object.profile_picture.url
            )
        )

    thumbnail.short_description = "Profile Picture"  # description for the picture
    list_display = ("thumbnail", "user", "city", "state", "country")


# register the model
admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
