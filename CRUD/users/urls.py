from django.urls import path
from . import views
from .views import user_list


urlpatterns = [
    path('create/', views.create_user, name='create_user'),
    path('', views.user_list, name='user_list'),
     path('', user_list, name='user_list'),
    path('update/<int:id>/', views.update_user, name='update_user'),
    path('delete/<int:id>/', views.delete_user, name='delete_user'),
]