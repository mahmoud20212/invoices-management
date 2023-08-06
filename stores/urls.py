from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<slug>/edit/', views.edit, name='edit'),
    path('<pk>/delete/', views.delete, name='delete'),
    path('<pk>/upload-excel/', views.upload_for_store, name='upload_for_store'),
    path('<pk>/delete-invoices/', views.delete_all_invoices, name='delete_all_invoices'),
]