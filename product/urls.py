from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<pk>/edit/', views.edit, name='edit'),
    path('<pk>/delete/', views.delete, name='delete'),
]