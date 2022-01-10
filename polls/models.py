from django.db import models
from users.models import CustomUser
from datetime import datetime

# Create your models here.
class Poll(models.Model):
    name  = models.CharField(max_length=200)
    description = models.TextField()
    expiry_date_time = models.DateTimeField()
    def poll_status(self):
        if datetime.now().replace(tzinfo=None) <= self.expiry_date_time.replace(tzinfo=None):
            return True
        else:
            return False
            
class Choice(models.Model): 
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    votes = models.IntegerField(default = 0)
    
class Comment(models.Model):
    poll = models.ForeignKey('Poll',on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class UserChoice(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    choice = models.ForeignKey('Choice', on_delete=models.CASCADE)