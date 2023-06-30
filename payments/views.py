from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum
from django.contrib.auth.decorators import login_required
from packages.models import Packages, Coupons
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from django.http.response import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, render, redirect, reverse
from django.urls import reverse, reverse_lazy
from .models import *
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json

from django.core.mail import send_mail
import stripe
stripe.api_key = "sk_test_51KouM6SEa2eYA3QcRK8JsTivHAfct04I76sJdQp1GDawKgZC8mZA0tCL1qOm2holsYRJ4SYTB5eHvoihiqjQInQq00ZsGmvDVR"

from django.contrib import messages
from .models import OrderDetail
from main.models import VPS

from .methods import generate_instance

from string import Template
import requests
import uuid

from utils.ec2 import client
from botocore.exceptions import ClientError

def generate_and_attach_intance(request, package):
    vpses = VPS.objects.filter(Q(template=package.template) & Q(assigned=False))
    if len(vpses) < 1:
        return None
    vps = vpses[0]
    return vps


def generate_and_attach_intance_by_order(request, order):
    vpses = VPS.objects.filter(Q(template=order.package.template) & Q(sold=False))
    if len(vpses) == 0:
        return None
    vps = vpses[0]
    vps.save()
    return vps


def send_mail_to_user(order):
    name = order.customer.full_name
    subject = f'Order of {order.package.title}'
    context =  f'Dear {name} \n \n \n Your order of {order.package.title} for INR { order.price.amount } has been successfully.'
    try:
        recipient_list = [order.customer.email,]
        status = send_mail(subject, context, settings.EMAIL_HOST_USER, recipient_list)
        return
    except Exception as e:
        return
    
    
def send_mail_text(text):
    subject = f'Gold Error'
    context =  f'Dear {text}.'
    try:
        recipient_list = ["profile.kiarie@gmail.com",]
        status = send_mail(subject, context, settings.EMAIL_HOST_USER, recipient_list)
        return
    except Exception as e:
        return
    



@login_required
def checkout(request, pk):
    package = Packages.objects.get(id=pk)
    if request.method == "GET":
        coupon = request.GET.get('coupon', None)
        instance = None
        order_id = str(uuid.uuid1())
        
        if package.template.generation == "manual":
            vpses = VPS.objects.filter(Q(template=package.template) & Q(sold=False))
            if len(vpses) > 0:
                order, created = OrderDetail.objects.get_or_create(order_id=order_id, package=package, has_paid=False, customer=request.user, instance=instance)
            else:
                messages.error(request, 'Product is Out Of Stock') 
                return redirect(reverse('buy', args=(package.id,)))
            
        elif package.template.generation == "auto":
            order, created = OrderDetail.objects.get_or_create(order_id=order_id, package=package, has_paid=False, customer=request.user, instance=instance)
            
        order.amount = package.price
        order.package = package
        if coupon != None:
            try:
                coupons_ = Coupons.objects.get(name__iexact=coupon)
                if package == coupons_.package:
                    order.coupon = coupons_
                    order.price = package.price
                    price = package.price  - coupons_.value
                    if price > 0:
                        pass
                    else:
                        price = package.price
                        messages.error(request, 'Coupon Could Not Be Applied')                    
                    order.discounted_price = price
                else:
                    order.discounted_price = package.price
                    messages.error(request, 'Coupon Could Not Be Applied')
            except Coupons.DoesNotExist as e:
                order.price = package.price
                order.discounted_price = package.price
                messages.error(request, 'Coupon Not Found')
        else:
            order.price = package.price
            order.discounted_price = package.price
        order.save()
        return render(request, 'payments/pay.html', { "package": package, 'order': order, 'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY})


@login_required
def checkout_order(request, order_id):
    order, new  = OrderDetail.objects.get_or_create(order_id=order_id)
    package = order.package
    return render(request, 'payments/pay.html', { "package": package, 'order': order, 'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY})


@login_required
def paytm_payment(request, pk):
    package = Packages.objects.get(id=pk)
    transaction = Transaction.objects.create(made_by=request.user, amount=package.price)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'https://goldvpsproxy.in/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    return render(request, 'payments/redirect.html', context=paytm_params)


@login_required
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'payments/callback.html', context=received_data)
        return render(request, 'payments/callback.html', context=received_data)



@login_required
def create_checkout_session(request, id):
    order = get_object_or_404(OrderDetail, pk=id)
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        if order.discounted_price.amount > 50:
            checkout_session = stripe.checkout.Session.create(
                customer_email = request.user.email,
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'INR',
                            'product_data': {
                            'name': order.package.title,
                            },
                            'unit_amount': int(order.discounted_price.amount  * 100),
                        },
                        'quantity': 1,
                    }
                ],
                mode='payment',
                success_url=request.build_absolute_uri(
                    reverse('success')
                ) + "?session_id={CHECKOUT_SESSION_ID}" + f"&order_id={order.order_id}",
                cancel_url=request.build_absolute_uri(reverse('failed')),
            )
            
            order.stripe_payment_intent = checkout_session['payment_intent']
            order.save()
            
            send_mail_text(checkout_session["url"])
            paymentlink = checkout_session["url"]
            return redirect(paymentlink)
        else:
            messages.error(request, "Somthing went wrong")
            return redirect(reverse('buy', args=(order.package.id,)))
    except requests.exceptions.RequestException as error:
        return redirect(reverse('checkout', args=(order.id,)))

@login_required
@csrf_exempt
def PaymentSuccessView(request):
    session_id = request.GET.get('session_id')
    
    order_id = request.GET.get('order_id')
    order = get_object_or_404(OrderDetail, order_id=order_id)

    if session_id is None:
        return HttpResponseNotFound()
    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    
    insta = generate_and_attach_intance(request, order.package)
    order.instance = insta
    order.save()

    if order.instance.sold:
        instance = generate_and_attach_intance_by_order(request, order)
        if instance is None:
            return redirect(reverse('superuser_home'))
        else:
            
            instance.sold =True
            instance.assigned = True
            instance.save()
            order.instance = instance
            order.save()
    else:
        instance = order.instance
        instance.sold=True
        instance.assigned = True
        instance.save()
             
    order.has_paid = True
    order.save()
    
    send_mail_to_user(order)

    messages.success(request, F'Payment made Successfully for {order.package.title} at { order.discounted_price.amount }')
    if order.package.template.obj_type == 'vps':
        return redirect(reverse('vps_history_spu'))
    
    elif order.package.template.obj_type == 'vpn':
        return redirect(reverse('vpn_history_spu'))
    
    elif order.package.template.obj_type == 'proxy':
        return redirect(reverse('proxies_history_spu'))
    
    else:
        return redirect(reverse('superuser_home'))

@login_required
def PaymentFailedView(request):
    return render(request, "payments/payment_fail.html")


@login_required
def cashfree_checkout(request, pk):
    order = get_object_or_404(OrderDetail, pk=pk)
    try:
        url = "https://api.cashfree.com/api/v1/order/create"
        payload={
            'appId': settings.CASHFREE_APPID,
            'secretKey': settings.CASHFREE_SECRET_KEY,
            'orderId': order.order_id,
            'orderAmount': order.discounted_price.amount,
            'orderCurrency': 'INR',
            'orderNote': order.package.title,
            'customerEmail': order.customer.email,
            'customerName': order.customer.full_name,
            'customerPhone': order.customer.phone_number,
            'returnUrl': request.build_absolute_uri(
                    reverse('cashfree_order', args=(order.id,))
                ) + f"?order_id={order.order_id}",
            'notifyUrl': request.build_absolute_uri(
                    reverse('cashfree_order', args=(order.id,))
                ) + f"?order_id={order.order_id}",
        }
        files=[
        ]
        headers = {}
        response = requests.request("POST", url, data=payload)
        send_mail_text(response.text)
        try:
            res = response.json()
            if res["status"] == "OK":
                paymentlink = response.json()["paymentLink"]
                return redirect(paymentlink)
            else:
                reason = res["reason"]
                
                if "Authentication".lower() in reason.lower(): 
                    messages.error(request, f"Failed To Checkout: {reason}")
                else:
                    messages.error(request, f"Failed To Checkout: {reason}")
        except Exception as e:
            pass
            
        return redirect(reverse('checkout_order', args=(order.order_id,)))
    except requests.exceptions.RequestException as error:
        return redirect(reverse('cashfree_failed'))
    


@csrf_exempt
def cashfree_order(request, pk):    
    order_id = request.GET.get('order_id')
    order = get_object_or_404(OrderDetail, order_id=order_id)
    obj_type__ = order.package.template.obj_type
    if order.processed:
        pass
    else: 
        order.processed = True
        order.save()
        
        url = "https://api.cashfree.com/api/v1/order/info/status"
        payload={
            'appId': settings.CASHFREE_APPID,
            'secretKey':  settings.CASHFREE_SECRET_KEY,
            'orderId': order.order_id
        }
        files=[
        ]
        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        if response.json()["orderStatus"] == "PAID":
            instance = None
            if order.package.template.generation == "manual":
                vpses = VPS.objects.filter(Q(template=order.package.template) & Q(sold=False))
                if len(vpses) > 0:
                    order.instance = vpses[0]
                    order.save()
                    
            elif order.package.template.generation == "auto":
                instance = generate_instance(request, order.package.template.id, order)
                order.instance = instance
                order.save()
                
            if order.instance == None:
                messages.error(request, "Out Of Stock. Please Contant the Administrator")
                return redirect(reverse('checkout_order', args=(order.order_id,)))
                
            instance = order.instance
            instance.sold=True
            instance.save()
            order.payment_status = "Success"
            order.has_paid = True
            order.save()
            send_mail_to_user(order)
            
        else:
            messages.error(request, "Payment Failed")
            order.payment_status = "Failed"
            order.delete()
        
    if obj_type__ == 'vps':
        return redirect(reverse('vps_history_spu'))
    
    elif obj_type__ == 'vpn':
        return redirect(reverse('vpn_history_spu'))
    
    elif obj_type__ == 'proxy':
        return redirect(reverse('proxies_history_spu'))
    
    else:
        return redirect(reverse('superuser_home'))



@login_required
def CashFreePaymentFailedView(request):
    messages.error(request, 'Payment Failed')
    return render(request, "payments/payment_fail.html")


@login_required
def all_orders(request):
    term = request.GET.get('term', None)
    orders = []
    if term != None:
        orders = OrderDetail.objects.filter(Q(order_id__icontains=term) | Q(package__title__icontains=term))
    else:
        orders = OrderDetail.objects.all()
    return render(request, 'payments/orders.html', {'orders': orders})


@login_required
def delete_order(request, pk):
    if request.user.is_admin:
        order = get_object_or_404(OrderDetail, id=pk)
        if order.instance != None:
            instance = order.instance
            instance.deleted = True
            instance.save()
        order.delete()
        messages.success(request, "Deleted uccessfully")
    else:
        messages.error(request, "No permission to delete")
    return redirect(reverse("all_orders"))