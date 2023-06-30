from django.urls import path
from .views import paytm_payment, all_orders,delete_order, callback, checkout, checkout_order, PaymentFailedView, PaymentSuccessView, cashfree_order,  create_checkout_session, cashfree_checkout, CashFreePaymentFailedView

urlpatterns = [
    
    #checkout
    path('checkout/<int:pk>', checkout, name="checkout"),
    path('checkout/order/<order_id>', checkout_order, name="checkout_order"),
    path('pay/<int:pk>', paytm_payment, name='pay'),
    path('callback/', callback, name='callback'),
    
    #stripe checkout
    path('success/', PaymentSuccessView, name='success'),
    path('failed/', PaymentFailedView, name='failed'),
    
    #cashfree checkout
    path('api/checkout-session/<id>/', create_checkout_session, name='api_checkout_session'),
    # path('stripe-payment/', stripe_payment, name='stripe_payment'),
    
    path('cashfree_checkout/<int:pk>', cashfree_checkout, name='cashfree_checkout'),
    path('order/success/<int:pk>', cashfree_order, name='cashfree_order'),

    path('cashfree_checkout/failed/', CashFreePaymentFailedView, name='cashfree_failed'),
    
    path('order_delete/<int:pk>', delete_order, name='delete_order'),
    path('orders/', all_orders , name='all_orders'),
]



