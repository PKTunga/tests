"""aws_p URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('authenticate.urls')),
    path('', include('payments.urls')),
    path('', include('main.urls')),
    path('', include('comply.urls')),
    path('', include('packages.urls')),
    path('referral/', include('referrals.urls')),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# def error_404(request, exception):
#    return render(request,'error.html')

# def error_500(request):
#    return render(request,'error.html')

# def error(request):
#    return render(request,'error.html')

# from django.conf.urls import handler404, handler500, handler403, handler400

# handler404 = error_404
# handler500 = error_500
# handler403 = error_404
# handler400 = error_404
