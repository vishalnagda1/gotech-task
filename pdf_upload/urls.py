from django.urls import path
from .views import signup, signin, signout, upload_file

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('upload/', upload_file, name='upload_file'),
]
