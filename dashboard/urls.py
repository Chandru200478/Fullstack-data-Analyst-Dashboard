from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('export-pdf/', views.export_pdf, name='export_pdf'),
]
