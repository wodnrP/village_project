from django.db import models
from user.models import CustomAbstractBaseUser
# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomAbstractBaseUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comments(models.Model):
    content = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    commenter = models.ForeignKey(CustomAbstractBaseUser, related_name="+", on_delete=models.CASCADE, blank=True)

    def __int__(self):
        return self.board