from django.shortcuts import render, redirect,reverse
from django.contrib.auth.decorators import login_required

from main.views import packages
from .forms import CouponForm, PackageForm
from .models import Coupons, Packages
from django.contrib import messages

@login_required
def add_package(request):
    if request.method == "POST":
        form = PackageForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('add_package'))
    return render(request, 'packages/add_package.html', {'form': PackageForm, 'packages': Packages.objects.all()})


@login_required
def edit_package(request, pk):
    instance = Packages.objects.get(id=pk)
    
    if request.method == "POST":
        form = PackageForm(request.POST, instance=instance)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('add_package'))
    context = {
        'form': PackageForm(instance=instance)
    }
    return render(request, 'packages/edit_package.html', context)

@login_required
def delete_package(request, pk):
    if request.user.is_admin:
        try:
          csv = Packages.objects.get(id=pk)
          csv.delete()
          messages.success(request, 'Delete Successful')
          return redirect(reverse('add_package'))
        except Exception as e:
          pass
    messages.error(request, "Delete Failed")
    return redirect(reverse('add_package'))



@login_required
def add_coupon(request):
    if request.method == "POST":
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('add_coupon'))
    return render(request, 'packages/add_coupon.html', {'form': CouponForm, 'coupons': Coupons.objects.all()})

@login_required
def edit_coupon(request, pk):
    instance = Coupons.objects.get(id=pk)

    if request.method == "POST":
        form = CouponForm(request.POST, instance=instance)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('add_coupon'))
    context = {
        'form': CouponForm(instance=instance)
    }
    return render(request, 'packages/edit_coupon.html', context)



@login_required
def delete_coupon(request, pk):
    if request.user.is_admin:
        try:
          csv = Coupons.objects.get(id=pk)
          csv.delete()
          messages.success(request, 'Delete Successful')
          return redirect(reverse('add_coupon'))
        except Exception as e:
          pass
    messages.error(request, "Delete Failed")
    return redirect(reverse('add_coupon'))
