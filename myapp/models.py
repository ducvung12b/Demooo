from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Create your models here.
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

class Pages(models.Model):
    title = models.CharField(max_length=100,null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE,null=True, blank=True)
    description = models.CharField(max_length=200,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Follow(models.Model): 
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE) 
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return f'{self.follower.username} follows {self.followed.username}'

class Notification(models.Model): 
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications') 
    sender = models.ForeignKey(User, on_delete=models.CASCADE) 
    page = models.ForeignKey(Pages, on_delete=models.CASCADE) 
    message = models.CharField(max_length=255) 
    read = models.BooleanField(default=False) 
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __str__(self): 
        return f'Notification for {self.recipient.username}'