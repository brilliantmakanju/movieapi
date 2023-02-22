from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    task = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    completed = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.task
    
    class Meta:
        ordering = ['-pk']

class Category(models.Model):
    category = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.category
    
    class Meta:
        ordering = ['-pk']

class Movie(models.Model):
    categories = models.CharField(max_length=255)
    title = models.CharField(max_length=255, null=False)
    short_desc = models.CharField(max_length=1000, null=False)
    full_desc = models.TextField(null=False)
    poster_pic = models.FileField(upload_to='VideoPoster')
    video_file = models.FileField(upload_to='Video')

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-pk']


class SavedMovie(models.Model):
    saved_by = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.movie.title
    
    class Meta:
        ordering = ['-pk']
