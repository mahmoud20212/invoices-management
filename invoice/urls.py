from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('create/', views.create, name='create'),
    path('<pk>/edit/', views.edit, name='edit'),
    path('<pk>/delete/', views.delete, name='delete'),
    path('<pk>/export/', views.export, name='export'),
    # path('<pk>/invoice/', views.show_invoice, name='show_invoice'),
    # path('<pk>/export-zip-file/', views.zip_invoices, name='zip_invoices'),
]