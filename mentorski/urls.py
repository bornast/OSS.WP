from django.urls import path

from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'mentorski'
urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('students/', views.students_page, name='students'),
    path('student_delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('subjects/', views.subjects_page, name='subjects'),
    path('subject_create/', views.create_subject, name='create_subjects'),
    path('subject_edit/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('subject_delete/<int:subject_id>/', views.delete_subject, name='delete_subject'),
    path('subject_view/<int:subject_id>/', views.view_subject, name='view_subject'),
    path('student_view/<int:student_id>/', views.view_student, name='view_student'),
    path('enroll_subject/<int:subject_id>/<int:student_id>/', views.enroll_subject, name='enroll_subject'),
    path('disenroll_subject/<int:subject_id>/<int:student_id>/', views.disenroll_subject, name='disenroll_subject'),
    path('mark_subject_as_passed/<int:subject_id>/<int:student_id>/', views.mark_subject_as_passed, name='mark_subject_as_passed'),    
    path('mark_subject_as_not_passed/<int:subject_id>/<int:student_id>/', views.mark_subject_as_not_passed, name='mark_subject_as_not_passed'),
]