from django.contrib import admin
from shop.models import Book, Review, ReadingProgress  # Виправлений імпорт

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'author')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at', 'updated_at')
    list_filter = ('rating', 'created_at')

@admin.register(ReadingProgress)
class ReadingProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)