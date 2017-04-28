# App Imports
import time
import models
import calendar

# Django Imports
from django.http import JsonResponse
from django.views.generic import ListView
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@csrf_exempt
def listener(request):
    if request.method == 'POST':
        response = JsonResponse(data={'success': True})
    else:
        response = JsonResponse(data={'success': False})
    return response

