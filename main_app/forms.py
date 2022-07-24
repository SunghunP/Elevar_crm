from dataclasses import fields
from django.forms import ModelForm
from .models import Contact, Account, Transactions

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'title', 'phone', 'email']

class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['company_name', 'industry', 'state', 'city', 'country', 'zip', 'description']

class TransactionForm(ModelForm):
    class Meta:
        model = Transactions
        fields = ['date', 'status', 'price']
