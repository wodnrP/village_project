from rest_framework import serializers
from .models import Vote, Choice

class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('id', 'board', 'title', 'create_time')

class ChoiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Choice
        fields = ('id', 'count', 'vote', 'content', 'voter')