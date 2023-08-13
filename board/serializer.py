from rest_framework import serializers
from .models import Board, Comments

class BoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = ('id', 'user', 'title', 'body', 'create_time')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('id', 'board', 'commenter', 'content', 'create_time')