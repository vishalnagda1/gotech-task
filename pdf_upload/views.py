from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import CustomUser


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = CustomUser.objects.create_user(username=username, password=password)
            return JsonResponse({'message': 'User created successfully'})
        except Exception as e:
            return JsonResponse({'message': 'Signup failed', 'exception': str(e)}, status=422)

