from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

class ReferralRelationship(models.Model):
    # who invite 
    inviter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='inviter',
        verbose_name="inviter",
        on_delete=models.CASCADE,
    )
    # who connected 
    invited = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='invited',
        verbose_name="invited",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    # referral code
    # refer_token = models.ForeignKey(
    #     "ReferralCode",
    #     verbose_name="referral_code",
    #     on_delete=models.CASCADE,
    # )
    refer_token = models.CharField(unique=True, max_length=150)
    date_created = models.DateField(_("Date created"), auto_now=True, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.inviter}_{self.invited}"

class ReferralCode(models.Model):
    token = models.CharField(unique=True, max_length=150)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="code_master", on_delete=models.CASCADE
    )
    def __str__(self) -> str:
        return f"{self.user}_{self.token}"
