from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth.decorators import login_required
from referrals.models import ReferralCode, ReferralRelationship
from authenticate.models import CustomUser

@login_required
def my_referrals(request):
    referrals = ReferralRelationship.objects.filter(inviter=request.user)
    return render(request, 'referrals/my_referrals.html', { "referrals": referrals, "link": request.build_absolute_uri(reverse('generate_referrals', args=(request.user.username, )))})

@login_required
def referrals(request):
    referrals = []
    if request.user.is_admin:
        referrals = ReferralRelationship.objects.all()
    return render(request, 'referrals/referrals.html', { "referrals": referrals})

@login_required
def filter_referrals(request, token):
    referrals = ReferralRelationship.objects.filter(inviter__referral_code=token)
    return render(request, 'referrals/referrals.html', { "referrals": referrals})

import uuid
def generate_referrals(request, username):
    if request.user.is_authenticated:
        return redirect('/')
    token = uuid.uuid4().hex
    user = get_object_or_404(CustomUser, username=username)
    referral = ReferralRelationship.objects.create(
        refer_token=token,
        inviter=user,
    )
    referral.save()
    # url = request.build_absolute_uri(f'/accounts/signup/?token={token}')
    return redirect(request.build_absolute_uri(f'/accounts/signup/?token={token}'))