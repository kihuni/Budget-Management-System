from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('user-register/', views.user_register, name='user-register'),
    path('', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('budgets/', login_required(views.BudgetListView.as_view()), name='budgets_list'),
    path('categories/', login_required(views.CategoryListView.as_view()), name='categories_list'),
    path('expenses/', login_required(views.ExpenseListView.as_view()), name='expenses_list'),
    path('incomes/', login_required(views.IncomeListView.as_view()), name='incomes_list'),
    path('transfers/', login_required(views.TransferListView.as_view()), name='transfers_list'),
]