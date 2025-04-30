from django.contrib import admin
from .models import Book, Review, CustomUser

admin.site.register(Book)
admin.site.register(Review)
admin.site.register(CustomUser)
