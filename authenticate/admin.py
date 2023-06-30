from django.contrib import admin

from .models import CustomUser, LoginMessage, LoggedInUser, WhatsappNumber

admin.site.register(CustomUser)
admin.site.register(LoginMessage)
admin.site.register(LoggedInUser)
admin.site.register(WhatsappNumber)