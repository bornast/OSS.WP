from django.urls import path

from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'mentorski'
urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('students/', views.students_page, name='students'),
    path('subjects/', views.subjects_page, name='subjects'),
    path('subject_create/', views.create_subject, name='create_subjects'),
    path('subject_edit/<int:subject_id>/', views.edit_subject, name='edit'),
    path('subject_delete/<int:subject_id>/', views.delete_subject, name='delete'),
    path('subject_view/<int:subject_id>/', views.view_subject, name='view'),
]