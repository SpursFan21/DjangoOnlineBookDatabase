from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    STATUS_CHOICES = [
        ('not-started', 'Not Started'),
        ('in-progress', 'In Progress'),
        ('complete', 'Complete')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate the book with a user
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    publisher = models.CharField(max_length=255)
    reading_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not-started')
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)  # For book cover image

    def __str__(self):
        return self.title
