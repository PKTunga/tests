from django.urls import path
from .views import add_coupon, add_package, edit_coupon, edit_package, delete_package, delete_coupon 


urlpatterns = [
    path('add_package', add_package, name="add_package"),
    path('add_coupon', add_coupon, name='add_coupon'),

    path('edit_package/<int:pk>', edit_package, name="edit_package"),
    path('edit_coupon/<int:pk>', edit_coupon, name='edit_coupon'),
    
    path('delete_package/<int:pk>', delete_package, name="delete_package"),
    path('delete_coupon/<int:pk>', delete_coupon, name='delete_coupon'),
]