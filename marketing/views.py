import json
import datetime

from django.conf import settings
from django.shortcuts import render, HttpResponse, Http404
from django.http import HttpResponseBadRequest
from django.utils import timezone

# Create your views here.
from .forms import EmailForm
from accounts.models import EmailMarketingSignUp

def dismiss_marketing_message(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {'success': True}
        json_data = json.dumps(data)
        request.session['dismiss_message_for'] = str(timezone.now() + \
            datetime.timedelta(hours=settings.MARKETING_HOURS_OFFSET,
                               minutes=settings.MARKETING_MINUTES_OFFSET,
                               seconds=settings.MARKETING_SECONDS_OFFSET))
        print(data)
        print(json_data)
        return HttpResponse(json_data, content_type='application/json')
    else:
        return Http404

def email_signup(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_signup, created = EmailMarketingSignUp.objects.get_or_create(email=email)
            request.session['email_added_marketing'] = True
            return HttpResponse('Success %s' % (email))
        if form.errors:
            json_data = json.dumps(form.errors)
            return HttpResponseBadRequest(json_data, content_type='application/json')
    else:
        return Http404
