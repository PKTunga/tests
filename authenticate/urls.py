from django.urls import path
from importlib import import_module
from django.urls import include, path
from allauth.socialaccount import providers
from allauth import app_settings
from django.urls import path, re_path
from authenticate import auth as allauth_views
from authenticate import views

urlpatterns = [
     path('settings', views.profile, name="settings" ),
     path('update_banner', views.update_banner, name="update_banner" ),
     path('update_rdp', views.update_rdp, name="update_rdp" ),
     path('update_banner_text', views.update_banner_text, name="update_banner_text" ),

     path('update_password', views.update_password, name="update_password" ),
     path('update_message', views.update_message, name="update_message" ),
     path('update_profile', views.update_profile, name="update_profile" ),
     path('u_update_password', views.light_update_password, name="light_update_password"),
     path('update_whatsapp', views.update_whatsapp, name="update_whatsapp" ),
     path('register/<token>', views.referral_signup, name="referral_signup"),
]

urlpatterns += [
    path("signup/", allauth_views.referral_signup, name="account_signup"),
    path("login/", allauth_views.login, name="account_login"),
    path("logout/", allauth_views.logout, name="account_logout"),
    path(
        "password/change/",
        allauth_views.password_change,
        name="account_change_password",
    ),
    path("password/set/", allauth_views.password_set, name="account_set_password"),
    path("inactive/", allauth_views.account_inactive, name="account_inactive"),
    # E-mail
    path("email/", allauth_views.email, name="account_email"),
    path(
        "confirm-email/",
        allauth_views.email_verification_sent,
        name="account_email_verification_sent",
    ),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        allauth_views.confirm_email,
        name="account_confirm_email",
    ),
    # password reset
    path("password/reset/", allauth_views.password_reset, name="account_reset_password"),
    path(
        "password/reset/done/",
        allauth_views.password_reset_done,
        name="account_reset_password_done",
    ),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        allauth_views.password_reset_from_key,
        name="account_reset_password_from_key",
    ),
    path(
        "password/reset/key/done/",
        allauth_views.password_reset_from_key_done,
        name="account_reset_password_from_key_done",
    ),
]


if app_settings.SOCIALACCOUNT_ENABLED:
    urlpatterns += [path("social/", include("allauth.socialaccount.urls"))]

# Provider urlpatterns, as separate attribute (for reusability).
provider_urlpatterns = []
for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + ".urls")
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, "urlpatterns", None)
    if prov_urlpatterns:
        provider_urlpatterns += prov_urlpatterns
urlpatterns += provider_urlpatterns



# uper User and ID not displaying in history
# delete redirect to different page - delete for VPS, history and manual and 
# edit redirect to other pages
# Enable 3proxy socks
# Azure copy