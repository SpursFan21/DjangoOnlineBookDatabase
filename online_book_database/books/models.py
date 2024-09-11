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

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Direct reference to Book model
    text = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(6)])  # Rating from 0 to 5

    def __str__(self):
        return f'Review for {self.book.title} by {self.user.username}'

