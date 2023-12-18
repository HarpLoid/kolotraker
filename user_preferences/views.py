from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages


def index(request):
    currencies = []

    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(file_path, 'r') as file:
        for currency in json.load(file):
            currencies.append(currency)

    pref_available = UserPreference.objects.filter(user=request.user).exists()
    user_preference = None

    if pref_available:
        user_preference = UserPreference.objects.get(user=request.user)

    if request.method == 'GET':
        return render(request, 'preferences/index.html', {'currencies': currencies,
                                                          'user_preference': user_preference})
    else:
        currency = request.POST['currency']
        if pref_available:
            user_preference.currency = currency
            user_preference.save()
        else:
            UserPreference.objects.create(user=request.user,
                                          currency=currency)
        messages.success(request, 'Your preferences has been updated')
        return render(request, 'preferences/index.html', {'currencies': currencies,
                                                          'user_preference': user_preference})
