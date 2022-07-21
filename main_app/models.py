from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
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
		return reverse('account_detail', kwargs={'account_id': self.id})


class Contact(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	title = models.CharField(max_length=100)
	phone = models.IntegerField()
	email = models.CharField(max_length=100)
	account = models.ForeignKey(Account, on_delete=models.CASCADE)

	def __str__(self):
		return f" This is {self.first_name}, {self.last_name}"

	def get_absolute_url(self):
		return reverse("contact_detail", kwargs={"contact_id": self.id})

class Product(models.Model):
	name = models.CharField(max_length=100)
	price = models.IntegerField()
	description = models.TextField(max_length=300)
	account = models.ForeignKey(Account, on_delete=models.CASCADE)

	def __str__(self):
		return f'Product {self.name} with a price of {self.price}'
	
	def get_absolute_url(self):
		return reverse('product_detail', kwargs = {'product_id': self.id})

class Photo(models.Model):
	url = models.CharField(max_length=200)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	def __str__(self):
		return f'Photo for product_id: {self.product_id} @{self.url}'
	