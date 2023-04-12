from django.db import models
from demo.models import User
# Create your models here.

class Post(models.Model) : 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    