from django.urls import path

from . import views

urlpatterns = [
     path('about-us', views.about_us, name="about_us" ),
     path('terms_and_conditions', views.terms_and_conditions, name="terms_and_conditions" ),
     path('refund-policy', views.refund_policy, name="refund" ),
     path('return-policy', views.return_policy, name="return" ),
     path('privacy-policy', views.privacy, name="privacy" ),
     path('contactus', views.contactUs, name="contact_us" ),
     path('purchase_flow', views.purchase_flow, name="purchase_flow" ),
     path('add_contact_details', views.add_contact_details, name="add_contact_details")
]
