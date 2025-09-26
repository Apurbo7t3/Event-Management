from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.CharField(blank=True,null=True)
    def __str__(self):
        return self.name

# class Participant(models.Model):
#     name=models.CharField(max_length=100)
#     email=models.EmailField(unique=True)
#     def __str__(self):
#         return self.name

class Event(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    date=models.DateField()
    time=models.TimeField()
    location=models.CharField(max_length=200)
    asset=models.ImageField(upload_to='event_assets',blank=True,null=True,default='event_assets/default_img.jpg')
    category=models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='events',
    )
    participants=models.ManyToManyField(
        User,
        related_name='events'
    )
    def __str__(self):
        return self.name
    


    