from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)


    def __str__(self):
        return self.user.username

class newsStory(models.Model):
    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=10, choices=[("pol", "Politics"), ("art", "Art"), ("tech", "Technology"), ("spo", "Sports"), ("trivia", "Trivia")])
    region = models.CharField(max_length=10, choices=[('uk', 'UK'), ('eu', 'Europe'), ('w', 'World')])
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateField()
    details = models.CharField(max_length=1000)

    def __str__(self):
        return self.headline