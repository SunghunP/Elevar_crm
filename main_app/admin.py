from django.contrib import admin
from .models import Product, Photo, Account, Contact
# Register your models here.
admin.site.register(Product)
admin.site.register(Photo)
admin.site.register(Account)
admin.site.register(Contact)