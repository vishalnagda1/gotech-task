from django.urls import path
from .views import signup, signin, signout, upload_file, list_files, rename_file, delete_file, download_file

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('upload/', upload_file, name='upload_file'),
    path('list/', list_files, name='list_files'),
    path('rename/<int:file_id>/', rename_file, name='rename_file'),
    path('delete/<int:file_id>/', delete_file, name='delete_file'),
    path('download/<int:file_id>/', download_file, name='download_file'),
]
