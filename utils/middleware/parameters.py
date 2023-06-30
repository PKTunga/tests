from django.conf import settings
from django.db import connection
from django.http import Http404
from django.urls import set_urlconf
from django.contrib.auth.models  import AnonymousUser 
from django.utils.deprecation import MiddlewareMixin

from django.forms.models import model_to_dict

import json
from comply.models import ContactDetails
from authenticate.models import WhatsappNumber

class ParametersMiddleware(MiddlewareMixin):
    """
    This middleware should be placed at the very top of the middleware stack.
    Selects the proper database schema using the request host. Can fail in
    various ways which is better than corrupting or revealing data.
    """
    def process_request(self, request):
        parameters = {}
        try:
            set_, new = ContactDetails.objects.get_or_create(id=1)
            info = model_to_dict(set_)
            
            w, new = WhatsappNumber.objects.get_or_create(id=1)
            
            parameters['address'] = info['address']
            parameters['phone_number'] = info['phone_number']
            parameters['email'] = info['email']
            parameters['whatsapp'] = f"https://wa.me/{w.number}"
            parameters['telegram'] = f"{w.link}"

        except ContactDetails.DoesNotExist:
            parameters['address'] = "Please Add Address"
            parameters['phone_number'] = "Please Add Phone Number"
            parameters['email'] = "Please Add Email"

        request.parameters = parameters
        

