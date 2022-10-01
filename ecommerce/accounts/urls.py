from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

# otp register views
from .views import (
    otp_register,
    otp_sign_in,
    otp_check,
    resent_otp,
    otp_confirm_signup,
    register,
    view_order_,
)

# admin views
from .views import (
    login,
    logout,
    register,
    admin_list_users,
    admin_home,
    admin_user_block,
    admin_user_enable,
    activate,
    admin_list_orders,
)

# user views
from .views import (
    dashboard,
    forgot_password,
    reset_password,
    my_orders,
    edit_profile,
    change_password,
    cancel_order,
    # cod_payment,
)

urlpatterns = [
    path("sign-up/", otp_register, name="register"),
    path("conform/", otp_confirm_signup, name="confirm"),
    path("otp-sign-in/", otp_sign_in, name="otp_user_login"),
    path("otp-check/", otp_check, name="otp_check"),
    path("resent-otp/", resent_otp, name="resent_otp"),
    path("logout/", logout, name="logout"),
    path("register/", register, name="regular_register"),  # currently hidden from user
    # user
    path("dashboard/", dashboard, name="dashboard"),
    path("my-orders/", my_orders, name="my_orders"),
    path("forgot-password/", forgot_password, name="forgot_password"),
    path("reset-password/", reset_password, name="reset_password"),
    path("edit-profile/", edit_profile, name="edit_profile"),
    path("view_order/<str:id>", view_order_, name="view_order_"),
    path("cancel-order/<str:order_number>", cancel_order, name="cancel_order"),
    path("change-password/", change_password, name="change_password"),
    # path("cod-payment/<str:order_number>", cod_payment, name="cod_payment"),
    # admin
    path("admin-login/", login, name="login"),
    path("admin-register/", register, name="admin-register"),
    path("activate/<uidb64>/<token>", activate, name="activate"),
    path("admin-home/", admin_home, name="admin_home"),
    path("admin-list-users/", admin_list_users, name="admin_list_users"),
    path("admin-list-orders/", admin_list_orders, name="admin_list_orders"),
    path("admin-disable-users/<int:id>", admin_user_block, name="admin_disable_user"),
    path("admin-enable-users/<int:id>", admin_user_enable, name="admin_enable_user"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
