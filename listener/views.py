# App Imports
import json
import models

# Django Imports
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def listener(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        event = models.Event.create_from_api(json_data)
        response = JsonResponse(data={'success': True, 'event': {'id': event.pk, 'userid': event.user_id}})
    else:
        response = JsonResponse(data={'success': False})
    return response

