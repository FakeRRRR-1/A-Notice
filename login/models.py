from django.db import models

# Create your models here.


class LoginData(models.Model):
    
    username = models.CharField("Username", max_length=30, unique=True)  
    password = models.CharField("Password", max_length=128)  
    email = models.EmailField("Email", unique=True) 
    