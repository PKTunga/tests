from django.db import models
from django.contrib.auth import get_user_model
from djmoney.models.fields import MoneyField
from django.shortcuts import reverse
User = get_user_model()

class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
    
    

from django.db import models
from django.core import validators

class OrderDetail(models.Model):

    id = models.BigAutoField(
        primary_key=True
    )
    
    customer_email = models.EmailField(
        verbose_name='Customer Email',
        null=True, 
        blank=True
    )
    
    customer = models.ForeignKey(
        to='authenticate.CustomUser',
        verbose_name='User',
        on_delete=models.CASCADE
    )
    instance = models.ForeignKey(
        to='main.VPS',
        verbose_name='iNSTANCE',
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )
    
    package = models.ForeignKey(
        to='packages.Packages',
        verbose_name='Package',
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )

    coupon = models.ForeignKey(
        to='packages.Coupons',
        verbose_name='Coupons',
        on_delete=models.SET_NULL,
        null=True, 
        blank=True
    )
    
    amount =  MoneyField(max_digits=14, decimal_places=2, default=0.00, default_currency='USD')
    price =  MoneyField(max_digits=14, decimal_places=2, default=0.00, default_currency='USD')
    discounted_price =  MoneyField(max_digits=14, decimal_places=2, default=0.00, default_currency='USD')
    token = models.CharField(
        max_length=200,
        null=True, 
        blank=True
    )
    
    payment_status = models.CharField(
        max_length=200,
        null=True, 
        blank=True,
        default="Pending"
    )
    
    order_id = models.CharField(
        max_length=200,
        null=True, 
        blank=True
    )

    stripe_payment_intent = models.CharField(
        max_length=200,
        null=True, 
        blank=True
    )
    paytm_payment_intent = models.CharField(
        max_length=200,
        null=True, 
        blank=True
    )
    has_paid = models.BooleanField(
        default=False,
        verbose_name='Payment Status'
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )
    updated_on = models.DateTimeField(
        auto_now_add=True
    )
    processed = models.BooleanField(default=False)
    
    
    
    @property
    def url(self):
        # return reverse('cashfree_checkout', args=(self.id))
        return ""
       
       
def order_date_function(instance):
    orders = OrderDetail.objects.filter(instance=instance)
    if orders.count() > 0:
        return orders.first().created_on
    return None
        