from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Stack(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) 
    last_quiz_timestamp = models.DateTimeField(null=True, blank=True)  # 

    def __str__(self):
        return self.name


class StackTag(models.Model):
    stack = models.ForeignKey(Stack, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    added_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('stack', 'tag')

    def __str__(self):
        return f"{self.stack.name} - {self.tag.name}"


class Card(models.Model):
    front = models.CharField(max_length=1000)
    back = models.CharField(max_length=1000)
    front_desc = models.CharField(max_length=1000, blank=True, null=True)
    back_desc = models.CharField(max_length=1000, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stack = models.ForeignKey(
        Stack, on_delete=models.CASCADE, related_name='cards')
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp field
    correct_answers = models.PositiveIntegerField(default=0)
    incorrect_answers = models.PositiveIntegerField(default=0)
    # TextField for 0/1 quiz results
    quiz_results = models.TextField(default='')
    last_quiz_timestamp = models.DateTimeField(blank=True, null=True)  # Timestamp of the last quiz

    def __str__(self):
        return f"{self.front} - {self.back}"


