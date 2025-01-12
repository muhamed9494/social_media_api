from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    """
    Custom User model that extends the base user functionality.
    Includes additional fields like profile picture and bio.
    """
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # `REQUIRED_FIELDS` should contain the fields that are required when creating a superuser through `createsuperuser`
    REQUIRED_FIELDS = ['email']  # The default fields are `username` and `password`, so just add others like `email` here if needed.

    def __str__(self):
        return self.username


class Follow(models.Model):
    """
    Represents a follow relationship between two users.
    Prevents users from following themselves.
    """
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')

    def save(self, *args, **kwargs):
        if self.follower == self.followed_user:
            raise ValidationError("Cannot follow yourself.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.follower.username} follows {self.followed_user.username}"


class Post(models.Model):
    """
    Represents a post made by a user.
    """
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"
