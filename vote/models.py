from django.db import models
from board.models import Board
# Create your models here.
class Vote(models.Model):
    title = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    board = models.OneToOneField(Board, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Choice(models.Model):
    count = models.IntegerField(default=0)
    content = models.CharField(max_length=100)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)

    def __str__(self):
        return self.vote