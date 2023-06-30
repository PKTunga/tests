from django.contrib import admin

from .models import VPS, Usage, Templates

admin.site.register(Usage)
admin.site.register(VPS)
admin.site.register(Templates)
