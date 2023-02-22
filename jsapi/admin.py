from django.contrib import admin
from .models import Todo, SavedMovie, Movie, Category

admin.site.register(Todo)
admin.site.register(Category)
admin.site.register(Movie)
admin.site.register(SavedMovie)