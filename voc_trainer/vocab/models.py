from django.db import models
from django.contrib.auth.models import User

class Stack(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp field

    def __str__(self):
        return self.name

class Card(models.Model):
    front = models.CharField(max_length=1000)
    back = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stack = models.ForeignKey(Stack, on_delete=models.CASCADE, related_name='cards')

    def __str__(self):
        return self.front



