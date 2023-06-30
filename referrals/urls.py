from django.urls import path
from .views import referrals, my_referrals, filter_referrals, generate_referrals

urlpatterns = [
    path('my_referrals', my_referrals, name="my_referrals"),
    path('filter_referrals/<token>', filter_referrals, name="filter_referrals"),
    path('', referrals, name="referrals"),
    path('<username>', generate_referrals, name="generate_referrals"),
]



