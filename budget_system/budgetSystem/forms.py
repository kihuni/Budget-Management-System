from django import forms
from .models import Budget, Category, Expense, Income, Transfer

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'start_date', 'end_date', 'max_spending_limit', 'target_savings']