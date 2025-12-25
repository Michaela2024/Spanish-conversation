from django.db import models
from django.contrib.auth.models import User

class Scenario(models.Model):
    name = models.CharField(max_length=200)
    context = models.TextField()
    language = models.CharField(max_length=50, default="Spanish")
    difficulty = models.CharField(max_length=50, default="beginner")
    vocab = models.JSONField(blank=True, null=True)
    role = models.CharField(max_length=100, default="Waiter")  # ← ADD THIS
    
    def __str__(self):
        return self.name

    
    def __str__(self):
        return f"{self.name} ({self.language})"

class Conversation(models.Model):
    """A user's conversation session"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.scenario.name}"

class Message(models.Model):
    """Individual messages in a conversation"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=[
        ('ai', 'AI'),
        ('user', 'User')
    ])
    content = models.TextField()
    feedback = models.TextField(blank=True)  # AI feedback on user's message
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']