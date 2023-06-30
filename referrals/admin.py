from django.contrib import admin

from referrals.models import ReferralCode, ReferralRelationship

admin.site.register(ReferralCode)
admin.site.register(ReferralRelationship)
