from django.contrib import admin
from shop.models import Book, Review, ReadingProgress, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'author')

admin.site.register(Review)
admin.site.register(ReadingProgress)