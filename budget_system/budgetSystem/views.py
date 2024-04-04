from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import BudgetForm, CustomUserCreationForm, CategoryForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Budget,Category,Expense,Income,Transfer

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
    return render(request, 'budgetSystem/register.html', {'login_form': form, 'register_form': UserCreationForm()})

def user_logout(request):
    logout(request)
    return redirect('login')  

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'budgetSystem/register.html', {'login_form': AuthenticationForm(), 'register_form': form})

@login_required
def dashboard(request):
    return render(request, 'budgetSystem/dashboard.html')

def register(request):
    return render(request, 'budgetSystem/register.html')

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