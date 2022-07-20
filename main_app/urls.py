from django.urls import path
from . import views

urlpatterns = [
    # home route
    path('', views.home, name='home'),
    # signup route
    path('accounts/signup/', views.signup, name='signup'),
]
