from django.urls import path
from . import views

urlpatterns = [

    # ==============================
    # PUBLIC ROUTES
    # ==============================
    path('', views.landing, name='landing'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),

    # ==============================
    # AUTH ROUTES
    # ==============================
    path('logout/', views.user_logout, name='logout'),

    # ==============================
    # MAIN APP ROUTES
    # ==============================
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),

    # ==============================
    # TASK ROUTES
    # ==============================
    path('add/', views.add_task, name='add_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),

]