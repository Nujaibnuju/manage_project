from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


class Project(models.Model):
    name        = models.CharField(max_length=255)
    description = models.TextField()
    created_by  = models.ForeignKey(User,on_delete=models.CASCADE, related_name="projects")
    created_at  = models.DateTimeField(auto_now_add=True)



class Task(models.Model):
    STATUS_CHOICES = (
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    )

    title       = models.CharField(max_length=255)
    description = models.TextField()
    status      = models.CharField(max_length=20,choices=STATUS_CHOICES, default='todo')
    project     = models.ForeignKey(Project,on_delete=models.CASCADE, related_name="tasks")
    assigned_to = models.ForeignKey(User,on_delete=models.CASCADE, related_name="tasks")
    due_date    = models.DateField()
    created_at  = models.DateTimeField(auto_now_add=True)