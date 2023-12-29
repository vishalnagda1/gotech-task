from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import json

from .models import CustomUser, UploadedFile
from .decorators import custom_login_required  # Import the custom decorator


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
            return JsonResponse({'message': 'Signup failed', 'exception': str(e)}, status=400)


@csrf_exempt
def signin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful'})
            else:
                return JsonResponse({'message': 'Login failed'}, status=401)
        except Exception as e:
            return JsonResponse({'message': 'Login failed', 'exception': str(e)}, status=400)


def signout(request):
    logout(request)
    return JsonResponse({'message': 'Signout successful'})


@csrf_exempt
@custom_login_required  # Use the custom decorator
def upload_file(request):
    if request.method == 'POST':
        try:
            user = request.user  # The @login_required decorator ensures the user is authenticated

            uploaded_file = request.FILES.get('file')

            # Check file size
            max_size = 10 * 1024 * 1024  # 10 MB in bytes
            if uploaded_file.size > max_size:
                return JsonResponse({'message': 'File size exceeds 10 MB limit'}, status=400)

            # Validate file type
            allowed_extensions = ['pdf', 'docx', 'jpeg', 'jpg']
            validator = FileExtensionValidator(allowed_extensions)
            try:
                validator(uploaded_file)
            except ValidationError as e:
                return JsonResponse({'message': 'Invalid file type', 'exception': str(e)}, status=400)

            # Save the uploaded file
            uploaded_file_instance = UploadedFile(user=user, file=uploaded_file)
            uploaded_file_instance.save()

            return JsonResponse({'message': 'File uploaded successfully'})
        except Exception as e:
            return JsonResponse({'message': 'File upload failed', 'exception': str(e)}, status=422)
