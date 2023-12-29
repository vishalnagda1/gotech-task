from django.contrib import admin

from .models import CustomUser, UploadedFile

admin.site.register(CustomUser)
admin.site.register(UploadedFile)
