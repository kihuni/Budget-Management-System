from django.db import models
from django.contrib.auth.models import User

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    max_spending_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    target_savings = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    date = models.DateField()
    location = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.category.name} ({self.budget.name})" 

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    source = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)

class Transfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    from_budget = models.ForeignKey(Budget, related_name='transfers_sent', on_delete=models.CASCADE)
    to_budget = models.ForeignKey(Budget, related_name='transfers_received', on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"From {self.from_budget.name} to {self.to_budget.name}" 
