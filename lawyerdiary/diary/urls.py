from django.urls import path
from . import views

urlpatterns = [
    path('', views.case_list, name='case_list'),
    path('add/', views.case_add, name='case_add'),
    path('<int:pk>/edit/', views.case_edit, name='case_edit'),
    path('<int:pk>/delete/', views.case_delete, name='case_delete'),
    path('download/excel/', views.download_excel, name='download_excel'),
    path('download/pdf/', views.download_pdf, name='download_pdf'),
]
