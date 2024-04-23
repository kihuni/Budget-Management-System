from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Budget, Category, Expense, Income, Transfer, UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'start_date', 'end_date', 'max_spending_limit', 'target_savings']
        

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'budget', 'date', 'location', 'notes']
        
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'date', 'source', 'notes']
        
class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['amount', 'date', 'from_budget', 'to_budget', 'notes']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']        