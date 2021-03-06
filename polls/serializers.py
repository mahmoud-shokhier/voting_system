from rest_framework import serializers
from .models import *

class ChoiceSerializer(serializers.ModelSerializer):
    choice_text = serializers.CharField(max_length=255)
    votes = serializers.IntegerField(default = 0)
    
    class Meta:
        model = Choice
        fields = ('choice_text', 'votes')


class PollSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200, min_length=2)
    description = serializers.CharField(max_length=255, min_length=2)
    expiry_date_time = serializers.DateTimeField()
    choices = serializers.SerializerMethodField()
    poll_status = serializers.BooleanField(read_only=True)
    
    def get_choices(self, instance):
        items = Choice.objects.filter(poll=instance)
        return ChoiceSerializer(items, many=True).data
    
    class Meta:
        model = Poll
        ordering = ('expiry_date_time',)
        fields = ('id', 'name', 'description', 'expiry_date_time', 'choices', 'poll_status')


class VoteSerializer(serializers.ModelSerializer):
    choice_id = serializers.IntegerField(min_value=1)
    poll_id = serializers.IntegerField(min_value=1)
    class Meta:
        model = UserChoice
        fields = ('id', 'poll_id', 'choice_id')
        

class CommentSerializer(serializers.ModelSerializer):
    poll_id = serializers.IntegerField(min_value=1)
    comment_text = serializers.CharField(max_length=255, min_length=2)
    class Meta:
        model = Comment
        fields = ('id', 'poll_id', 'comment_text')
        
