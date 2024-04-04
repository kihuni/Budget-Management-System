from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('user-register/', views.user_register, name='user-register'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('budgets/', login_required(views.BudgetListView.as_view()), name='budgets_list'),
    path('categories/', login_required(views.CategoryListView.as_view()), name='categories_list'),
]