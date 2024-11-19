from django.urls import path
from .views import index
from .views import user_info_view

urlpatterns = [
    path('', index, name='index'),
    path('user_info/', user_info_view, name='user_info'),
]