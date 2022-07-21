from ast import Del
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Account, Contact, Photo, Product

S3_BASE_URL = ''
BUCKET = ''

# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invaild sign up - try again"
    form = UserCreationForm()
    context = {'form': form, "error_message": error_message}
    return render(request, 'registration/signup.html', context)

################
## Account Views
################

@login_required
def account_index(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'account/index.html', {'accounts': accounts})


@login_required
def account_detail(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if not account.user == request.user:
        return redirect('home')
    ## todo! populate all employees belonging to this account
    # employees = Contact.objects.filter(company_id = account_id)
    return render(request, 'account/detail.html', {
        'account': account,
        # 'employees': employees
        })


class AccountCreate(LoginRequiredMixin, CreateView):
    model = Account
    fields = ['company_name', 'industry', 'state', 'city', 'country', 'zip', 'description']

    def form_valid(self, form):
        ## this is assigning the logged in user 
        form.instance.user = self.request.user
        return super().form_valid(form)

class AccountUpdate(LoginRequiredMixin, UpdateView):
    model = Account
    fields = ['company_name', 'industry', 'state', 'city', 'country', 'zip', 'description']

    def get_object(self, queryset=None):
        account = super(AccountUpdate, self).get_object()
        if not account.user == self.request.user:
            return redirect('home')
        return account


class AccountDelete(LoginRequiredMixin, DeleteView):
    model = Account
    success_url = '/account/'

    def get_object(self, queryset=None):
        account = super(AccountDelete, self).get_object()
        if not account.user == self.request.user:
            return redirect('home')
        return account
################
## Contact Views
################
class ContactList(LoginRequiredMixin, ListView):
    model = Contact

    def get_object(self, queryset=None):
        contact = super(ContactList, self).get_object()
        if not contact.account == self.request.account:
            return redirect('home')
        return contact


class ContactDetail(LoginRequiredMixin, DetailView):
    model = Contact

    #todo! authorization logic needed 
    # def get_object(self, queryset=None):
    #     contact = super(ContactDetail, self).get_object()
    #     if not contact.account == self.request.account:
    #         return redirect('home')
    #     return contact

class ContactCreate(LoginRequiredMixin, CreateView):
    model = Contact
    fields = ['first_name', 'last_name', 'title', 'phone', 'email']

class ContactUpdate(LoginRequiredMixin, UpdateView):
    model = Contact
    fields = ['first_name', 'last_name', 'title', 'phone', 'email']

class ContactDelete(LoginRequiredMixin, DeleteView):
    model = Contact
    success_url = '/contact/'




#################
## Product Views
#################
class ProductList(LoginRequiredMixin, ListView):
    model = Product

    def get_object(self, queryset=None):
        product = super(ProductList, self).get_object()
        if not product.account == self.request.account:
            return redirect('home')
        return product


class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product

class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'price', 'description']

class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'price', 'description']


class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = '/product/'
