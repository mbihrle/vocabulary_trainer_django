from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Stack(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp field
    last_quiz_timestamp = models.DateTimeField(null=True, blank=True)  # Add this field

    def __str__(self):
        return self.name


class Card(models.Model):
    front = models.CharField(max_length=1000)
    back = models.CharField(max_length=1000)
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

    # def record_quiz_result(self, is_correct):
    #     """Record the result of a quiz attempt."""
    #     if is_correct:
    #         self.correct_answers += 1
    #         result = '1'  # Correct answer
    #     else:
    #         self.incorrect_answers += 1
    #         result = '0'  # Incorrect answer

    #     # Update the quiz results text field
    #     if self.quiz_results:
    #         self.quiz_results += result
    #     else:
    #         self.quiz_results = result

    #     # Update the timestamp of the last quiz attempt
    #     self.last_quiz_timestamp = timezone.now()

    #     # Save the changes to the model
    #     self.save()
