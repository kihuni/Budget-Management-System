from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import BudgetForm, CustomUserCreationForm, CategoryForm, ExpenseForm, IncomeForm, TransferForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Budget,Category,Expense,Income,Transfer
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.db.models import Sum
from .models import Expense
import datetime

from .models import *

# Create your views here.

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
        print("Rendering login page")
    return render(request, 'budgetSystem/login.html', {'login_form': form, 'register_form': UserCreationForm()})

def user_logout(request):
    logout(request)
    return redirect('register')  

def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'budgetSystem/user-register.html', {'login_form': AuthenticationForm(), 'register_form': form})

@login_required
def dashboard(request):
    return render(request, 'budgetSystem/dashboard.html')

def register(request):
    return render(request, 'budgetSystem/register.html')
    print('hi there i am in register')


def generate_pdf_report(request):
    # Get current month and year
    today = datetime.date.today()
    month = today.month
    year = today.year

    # Retrieve expenses for the current month
    expenses = Expense.objects.filter(date__month=month, date__year=year)

    # Aggregate total spending for each category
    spending_by_category = expenses.values('category__name').annotate(total_spent=Sum('amount'))

    # Create PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="monthly_spending_report_{month}_{year}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Add title to the document
    elements.append("Monthly Spending Report\n\n")

    # Create table with spending data
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

    # Build PDF document
    doc.build(elements)
    return response

class BudgetListView(LoginRequiredMixin,ListView):
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
        
        
class CategoryListView(LoginRequiredMixin,ListView):
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

class ExpenseListView(LoginRequiredMixin,ListView):
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
  

class IncomeListView(LoginRequiredMixin,ListView):
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
        
class TransferListView(LoginRequiredMixin,ListView):
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
    
            