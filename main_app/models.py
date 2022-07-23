from django.db import models
from django.forms import IntegerField
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Product(models.Model):
	name = models.CharField(max_length=100)
	price = models.IntegerField()
	description = models.TextField(max_length=300)

	def __str__(self):
		return f'Product {self.name} with a price of {self.price}'
	
	def get_absolute_url(self):
		return reverse('product_detail', kwargs = {'pk': self.id})

class Account(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	products = models.ManyToManyField(Product)
	company_name = models.CharField(max_length=100)
	industry = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	country = models.CharField(max_length=100)
	zip = models.IntegerField()
	description = models.TextField(max_length=250)

	def __str__(self):
		return f"company {self.company_name} located in {self.city}/{self.state}"

	def get_absolute_url(self):
		return reverse('account', kwargs={'account_id': self.id}) 


class Contact(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	title = models.CharField(max_length=100)
	phone = PhoneNumberField(unique = True, null = False, blank = False)
	email = models.CharField(max_length=100)
	account = models.ForeignKey(Account, on_delete=models.CASCADE)

	def __str__(self):
		return f" This is {self.first_name}, {self.last_name}"

	def get_absolute_url(self):
		return reverse("contact_detail", kwargs={"pk": self.id})


class Photo(models.Model):
	url = models.CharField(max_length=200)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	def __str__(self):
		return f'Photo for product_id: {self.product_id} @{self.url}'

# Transaction Model
# class Transactions(models.Model):
# 	serial_number = IntegerField()
# 	date = models.DateField('transaction date')
# 	price = models.IntegerField()
# 	account = models.ForeignKey(Account, on_delete=models.CASCADE)