from django.contrib.auth import views as auth_views
from django.urls import path
from .views import generate_pdf_report,landing_page, user_login, user_logout, user_register, dashboard, BudgetListView, CategoryListView, ExpenseListView, IncomeListView, TransferListView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', landing_page, name='landing_page'),
    path('user-register/', user_register, name='user-register'),
    path('dashboard/', login_required(dashboard), name='dashboard'),
    path('budgets/', login_required(BudgetListView.as_view()), name='budgets_list'),
    path('categories/', login_required(CategoryListView.as_view()), name='categories_list'),
    path('expenses/', login_required(ExpenseListView.as_view()), name='expenses_list'),
    path('incomes/', login_required(IncomeListView.as_view()), name='incomes_list'),
    path('transfers/', login_required(TransferListView.as_view()), name='transfers_list'),
    path('generate-pdf/<str:period>/', generate_pdf_report, name='generate_pdf_report'),
]