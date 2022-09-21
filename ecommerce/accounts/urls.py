from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import otp_register, otp_sign_in, otp_check, resent_otp, otp_confirm_signup, register
from .views import login, logout, register
urlpatterns = [
    path('sign-up/', otp_register, name='register'),
    path('conform/', otp_confirm_signup, name='confirm'),
    path('otp-sign-in/', otp_sign_in, name='otp_user_login'),
    path('otp-check/', otp_check, name='otp_check'),
    path('resent-otp/', resent_otp, name='resent_otp'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='regular_register'),  # currently hidden from user
    # admin
    path('admin-login/', login, name='login'),
    path('admin-register/', register, name='admin-register'),
    # sites


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
