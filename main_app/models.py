from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
	name = models.CharField(max_length=100)
	price = models.IntegerField()
	description = models.TextField(max_length=300)

	def __str__(self):
		return f'Product {self.name} with a price of {self.price}'
	
	def get_absolute_url(self):
		return reverse('detail', kwargs = {'product_id': self.id})

class Photo(models.Model):
	url = models.CharField(max_length=200)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	def __str__(self):
		return f'Photo for product_id: {self.product_id} @{self.url}'