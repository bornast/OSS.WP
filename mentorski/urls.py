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
    # path('login/', LoginView.as_view(template_name='login.html'), name='login'),
]