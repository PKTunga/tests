from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.core.mail import send_mail
from django.conf import settings
from comply.models import ContactDetails


from django.contrib.auth.decorators import login_required

from main.forms import ContactForm
from .forms import ContactDetailsForm




def contactUs(request):
    if request.method == "POST":
        name = request.POST.get('full_name')
        phone = request.POST.get('phone_number')
        email = request.POST.get('email_address')
        message = request.POST.get('message')
        subject = request.POST.get('subject')
        context =  f'{name} of {phone} and email {email} contacted you about {subject}. Detailed message {message}'

        try:
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_HOST_USER,]
            status = send_mail(subject, context, settings.EMAIL_HOST_USER, recipient_list)
            messages.success(request, "Request received. We will get back to you.")

        except Exception as e:
            print(e)

            messages.success(request, "Failed. Please try again.")

    return render(request, 'comply/contact_us.html', {'form': ContactForm()})


@login_required
def add_contact_details(request):
    instance, new = ContactDetails.objects.get_or_create(id=1)
    context = {}
    if request.method == "POST":
        form = ContactDetailsForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            
    context["form"] = ContactDetailsForm(instance=instance)
    return render(request, 'comply/add_contact_details.html', context)


def about_us(request):
    return render(request, 'comply/about_us.html')


def terms_and_conditions(request):
    return render(request, 'comply/terms.html')


def return_policy(request):
    return render(request, 'comply/return.html')


def refund_policy(request):
    return render(request, 'comply/refund.html')


def privacy(request):
    return render(request, 'comply/provacy.html')


def purchase_flow(request):
    return render(request, 'comply/flow.html')