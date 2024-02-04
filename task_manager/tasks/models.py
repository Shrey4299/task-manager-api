from django.db import models
from users.models import RegisterUser

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
