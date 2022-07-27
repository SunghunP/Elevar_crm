from ast import Del
from dataclasses import fields
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Account, Contact, Photo, Product, Transaction
from .forms import ContactForm, AccountForm, TransactionForm
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from chartjs.views.columns import BaseColumnsHighChartsView
import environ


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Apple", "Google", "Symmetra"]

    def get_data(self):
        """Return 3 datasets to plot."""
        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]


class ColumnHighChartJSONView(BaseColumnsHighChartsView):
    title = "Column Highchart test"
    yUnit = "%"
    providers = ["All"]
    credits = {"enabled": False}


env = environ.Env()
environ.Env.read_env()
line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()

env = environ.Env()
environ.Env.read_env()

S3_BASE_URL = 'https://s3.us-west-2.amazonaws.com/'
BUCKET = env('S3_PICTURES_BUCKET')

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'home.html')


@login_required
def dashboard(request):
    # todo transactions go here
    return render(request, 'dashboard.html')


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
    account_form = AccountForm()
    return render(request, 'account/index.html', {
        'accounts': accounts,
        'account_form': account_form,
    })


@login_required
def account_detail(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    #todo! rendering product in details page
    if not account.user == request.user:
        return redirect('home')
    transaction_form = TransactionForm()
    contact_form = ContactForm()
    products = Product.objects.all()
    employees = Contact.objects.filter(account_id=account_id)
    product_not_in_acc = Product.objects.exclude(id__in = account.products.all().values_list('id'))

    return render(request, 'account/detail.html', {
        'account': account,
        'employees': employees,
        'contact_form': contact_form,
        'transaction_form': transaction_form,
        'products': products,
        'prod' : product_not_in_acc,
    })


@login_required
def account_create(request):
    form = AccountForm(request.POST)
    if form.is_valid():
        new_contact = form.save(commit=False)
        new_contact.user = request.user
        new_contact.save()
    return redirect('account_index')


class AccountUpdate(LoginRequiredMixin, UpdateView):
    model = Account
    fields = ['company_name', 'industry', 'state',
              'city', 'country', 'zip', 'description']

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


def contact_create(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if not account.user == request.user:
        return redirect('home')
    form = ContactForm(request.POST)
    if form.is_valid():
        new_contact = form.save(commit=False)
        new_contact.account_id = account_id
        new_contact.save()
    return redirect('account_detail', account_id=account_id)


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


@login_required
def add_photo(request, product_id):
    # todo product authorization
    # product = Product.objects.get(id=product_id, user=request.user)
    # if not product.user == request.user:
    #     return redirect('home')
    # return product
    # photo-file will be the 'name' attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    print(f"this is photo_file -->> {photo_file}")
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique 'key' for s3 / needs file extension
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.')]
        print(f"this is key -->> {key}")
        # error handling
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, product_id=product_id)
            print(f"this is photo in try block -->> {photo}")
            photo.save()
        except:
            print('An error occured')
    return redirect("product_detail", pk=product_id)


@login_required
def assoc_product(request, account_id, product_id):
    Account.objects.get(
        id=account_id, user=request.user).products.add(product_id)
    return redirect('account_detail', account_id=account_id)


@login_required
def remove_product(request, account_id, product_id):
    Account.objects.get(
        id=account_id, user=request.user).products.remove(product_id)
    return redirect('account_detail', account_id=account_id)

#########################
## Transaction
#########################


@login_required
def add_transaction(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if not account.user == request.user:
        return redirect('home')
    form = TransactionForm(request.POST)
    if form.is_valid():
        new_transaction = form.save(commit=False)
        new_transaction.account_id = account_id
        new_transaction.serial_number = uuid.uuid4().hex[:10]
        new_transaction.save()
    return redirect('account_detail', account_id=account_id)


class TransactionUpdate(LoginRequiredMixin, UpdateView):
    model = Transaction
    fields = ['status']
    
    def get_success_url(self):
        return reverse("account_detail", kwargs={"account_id": self.object.account_id}) 
