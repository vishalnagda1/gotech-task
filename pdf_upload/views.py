from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from PIL import Image
import fitz  # PyMuPDF
import json
import os
import io
# from django.core.files.base import ContentFile
# from django.core.files.storage import default_storage

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
            user = request.user

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


@custom_login_required
def list_files(request):
    user = request.user
    files = UploadedFile.objects.filter(user=user)
    
    file_list = [{'file_id': file.id, 'file_name': os.path.basename(file.file.name)} for file in files]
    
    return JsonResponse({'files': file_list})


@csrf_exempt
@custom_login_required
def rename_file(request, file_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            new_name = data.get('new_name')

            # Ensure the new_name is not None
            if new_name is None:
                return JsonResponse({'message': 'New file name cannot be None'}, status=400)

            user = request.user

            # Check if the file belongs to the authenticated user
            uploaded_file = UploadedFile.objects.get(id=file_id, user=user)

            # Get the current content of the file
            file_content = uploaded_file.file.read()

            # Close the file before renaming
            uploaded_file.file.close()

            # Rename the file using Storage's move method
            new_file_name = os.path.join(settings.MEDIA_ROOT, 'uploads', new_name)
            # new_file_path = default_storage.save(new_file_name, ContentFile(file_content))

            # if default_storage.exists(uploaded_file.file.path):
            #     default_storage.delete(uploaded_file.file.path)

            # # Update the file field with the new path
            # uploaded_file.file.name = new_file_path
            print("uploaded_file.file.path:", uploaded_file.file.path)
            os.rename(uploaded_file.file.path, new_file_name)
            uploaded_file.file.name = new_file_name
            uploaded_file.save()

            return JsonResponse({'message': 'File renamed successfully'})
        except UploadedFile.DoesNotExist:
            return JsonResponse({'message': 'File not found or does not belong to the user'}, status=404)
        except Exception as e:
            return JsonResponse({'message': 'File rename failed', 'exception': str(e)}, status=422)


@csrf_exempt
@custom_login_required
def delete_file(request, file_id):
    if request.method == 'DELETE':
        try:
            user = request.user

            # Check if the file belongs to the authenticated user
            uploaded_file = UploadedFile.objects.get(id=file_id, user=user)

            # Delete the file
            uploaded_file.file.delete()
            uploaded_file.delete()

            return JsonResponse({'message': 'File deleted successfully'})
        except UploadedFile.DoesNotExist:
            return JsonResponse({'message': 'File not found or does not belong to the user'}, status=404)
        except Exception as e:
            return JsonResponse({'message': 'File deletion failed', 'exception': str(e)}, status=422)


@custom_login_required
def download_file(request, file_id):
    try:
        user = request.user

        # Check if the file belongs to the authenticated user
        uploaded_file = UploadedFile.objects.get(id=file_id, user=user)

        # Prepare the file for download
        file_path = uploaded_file.file.path
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    except UploadedFile.DoesNotExist:
        return JsonResponse({'message': 'File not found or does not belong to the user'}, status=404)
    except Exception as e:
        return JsonResponse({'message': 'File download failed', 'exception': str(e)}, status=422)


@csrf_exempt
@custom_login_required
def extract_images_and_text(request, file_id):
    if request.method == 'POST':
        try:
            user = request.user

            # Check if the file belongs to the authenticated user
            uploaded_file = UploadedFile.objects.get(id=file_id, user=user)

            # Get the file path
            file_path = uploaded_file.file.path

            # Extract images
            images = extract_images_from_pdf(file_path)

            # Extract text
            text = extract_text_from_pdf(file_path)

            return JsonResponse({'images': images, 'text': text})
        except UploadedFile.DoesNotExist:
            return JsonResponse({'message': 'File not found or does not belong to the user'}, status=404)
        except Exception as e:
            return JsonResponse({'message': 'Extraction failed', 'exception': str(e)}, status=500)


# Helper functions

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def extract_images_from_pdf(pdf_path):
    images = []
    pdf_document = fitz.open(pdf_path)

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        images_in_page = page.get_images(full=True)
        
        for img_index, img_info in enumerate(images_in_page):
            image_index = img_info[0]
            base_image = pdf_document.extract_image(image_index)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))

            # Ensure the directory exists before saving the image
            save_directory = os.path.join(settings.MEDIA_ROOT, "extracted_images")
            ensure_directory_exists(save_directory)

            image_path = os.path.join(save_directory, f"page_{page_num + 1}_img_{img_index + 1}.png")
            image.save(image_path)
            images.append(image_path)

    return images


def extract_text_from_pdf(pdf_path):
    text = ""
    pdf_document = fitz.open(pdf_path)

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text += page.get_text()

    return text
