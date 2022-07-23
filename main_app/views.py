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
from .forms import ContactForm

S3_BASE_URL = 'https://s3.us-west-2.amazonaws.com/'
BUCKET = 'elevar-crm-project'

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
    #todo! rendering product in details page
    # product = Product.objects.get(id=product_id, user=request.user)

    if not account.user == request.user:
        return redirect('home')
    contact_form = ContactForm()
    employees = Contact.objects.filter(account_id = account_id)
    return render(request, 'account/detail.html', {
        'account': account,
        'employees': employees,
        'contact_form': contact_form,
        # 'product' : product,
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
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.')]
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