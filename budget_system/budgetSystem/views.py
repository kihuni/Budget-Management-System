from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import BudgetForm, CustomUserCreationForm, CategoryForm, ExpenseForm, IncomeForm, TransferForm, UserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Budget, Category, Expense, Income, Transfer, UserProfile
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from django.db.models import Sum
import datetime

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'budgetSystem/login.html', {'login_form': form, 'register_form': UserCreationForm()})

def user_logout(request):
    logout(request)
    return redirect('landing_page')  

def user_register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
    else:
        user_form = CustomUserCreationForm()
        profile_form = UserProfileForm()
    return render(request, 'budgetSystem/user-register.html', {'user_form': user_form, 'profile_form': profile_form})

def landing_page(request):
    return render(request, 'budgetSystem/landing_page.html')

@login_required
def dashboard(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None
    return render(request, 'budgetSystem/dashboard.html', {'user': user, 'user_profile': user_profile})

def generate_pdf_report(request, period='monthly'):
    today = datetime.date.today()

    if period == 'monthly':
        month = today.month
        year = today.year
        start_date = datetime.date(year, month, 1)
        if month == 12:
            end_date = datetime.date(year + 1, 1, 1)
        else:
            end_date = datetime.date(year, month + 1, 1)

    elif period == 'weekly':
        start_date = today - datetime.timedelta(days=today.weekday())
        end_date = start_date + datetime.timedelta(days=6)

    expenses = Expense.objects.filter(date__range=[start_date, end_date])
    spending_by_category = expenses.values('category__name').annotate(total_spent=Sum('amount'))

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{period}_spending_report_{start_date}_{end_date}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    elements.append(Paragraph("Monthly Spending Report\n\n", style=None))

    data = [['Category', 'Total Spent']]
    for item in spending_by_category:
        data.append([item['category__name'], item['total_spent']])
    
    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    elements.append(table)

    doc.build(elements)
    return response

class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'budgetSystem/budget_list.html'
    context_object_name = 'budgets'
    ordering = ['-start_date']
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['budget_form'] = BudgetForm()
        return context

    def post(self, request, *args, **kwargs):
        budget_form = BudgetForm(request.POST)
        if budget_form.is_valid():
            budget = budget_form.save(commit=False)
            budget.user = request.user
            budget_form.save()
            return redirect('budgets_list')
        else:
            return render(request, self.template_name, {'budgets': self.get_queryset(), 'budget_form': budget_form})
        
        
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'budgetSystem/category_list.html'
    context_object_name = 'categories'
    ordering = ['name']
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_form'] = CategoryForm()
        return context

    def post(self, request, *args, **kwargs):
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category = category_form.save(commit=False)
            category.user = request.user
            category_form.save()
            return redirect('categories_list')
        else:
            return render(request, self.template_name, {'categories': self.get_queryset(), 'category_form': category_form})

class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'budgetSystem/expense_list.html'
    context_object_name = 'expenses'
    ordering = ['-date']
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expense_form'] = ExpenseForm()
        return context

    def post(self, request, *args, **kwargs):
        expense_form = ExpenseForm(request.POST)
        if expense_form.is_valid():
            expense = expense_form.save(commit=False)
            expense.user = request.user
            expense_form.save()
            return redirect('expenses_list')
        else:
            return render(request, self.template_name, {'expenses': self.get_queryset(), 'expense_form': expense_form})
  

class IncomeListView(LoginRequiredMixin, ListView):
    model = Income
    template_name = 'budgetSystem/income_list.html'
    context_object_name = 'incomes'
    ordering = ['-date']
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['income_form'] = IncomeForm()
        return context

    def post(self, request, *args, **kwargs):
        income_form = IncomeForm(request.POST)
        if income_form.is_valid():
            income = income_form.save(commit=False)
            income.user = request.user
            income_form.save()
            return redirect('incomes_list')
        else:
            return render(request, self.template_name, {'incomes': self.get_queryset(), 'income_form': income_form})
class TransferListView(LoginRequiredMixin, ListView):
    model = Transfer
    template_name = 'budgetSystem/transfer_list.html'
    context_object_name = 'transfers'
    ordering = ['-date']
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transfer_form'] = TransferForm()
        return context
    
    def post(self, request, *args, **kwargs):
        transfer_form = TransferForm(request.POST)
        if transfer_form.is_valid():
            transfer = transfer_form.save(commit=False)
            transfer.user = request.user
            transfer_form.save()
            return redirect('transfers_list')
        else:
            return render(request, self.template_name, {'transfers': self.get_queryset(), 'transfer_form': transfer_form})
