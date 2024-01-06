from django.db import models
from django.contrib.auth.models import User
from django import forms 
from django.utils import timezone

class User(models.Model):
    id=models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=100,default="null")
    lastname = models.CharField(max_length=100,default="null")
    phone=models.CharField(max_length=10,default="0000000000")
    email = models.EmailField(max_length=254,default="null")
    password = models.CharField(max_length=100,default="null")
  
    def __str__(self):
        return self.firstname
    
# tasks/models.py

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Set a default user ID (replace with a valid user ID)
    title = models.CharField(max_length=100, default="null")
    description = models.TextField(max_length=300, default="null")
    date_created = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title