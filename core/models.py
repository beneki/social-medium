from django.db import models
from django.contrib.auth import get_user_model
from .utility import ULIDField 
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    id = ULIDField(primary_key=True)
    user = models.CharField(max_length=100)
    img = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user
    

class LikePost(models.Model):
    post_id = models.CharField(max_length=26)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self) -> str:
        return super().__str__()