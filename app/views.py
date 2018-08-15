from django.shortcuts import render
from django.db import models

from app.models.models import User


# Create your views here.
def home(request):
    user_list = User.objects.get(pk=1)
    print(user_list)
    return render(request, 'home.html')

    
def user(request):
    return render(request, 'user.html')
