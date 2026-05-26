from django.shortcuts import render, get_object_or_404
from shop.models import Book, Category


# 1. Головна сторінка
def index_view(request):
    context = {
        'title': 'Головна — Каталог',
        'categories': Category.objects.all(),
        'books': Book.objects.all(),
    }
    return render(request, 'index.html', context)


# 2. Сторінка конкретного жанру (категорії)
def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    books_in_category = Book.objects.filter(category=category)

    context = {
        'title': f"Жанр: {category.name}",
        'category': category,
        'categories': Category.objects.all(),
        'books': books_in_category
    }
    return render(request, 'category.html', context)


# 3. Сторінка окремої книги (деталі товару)
def book_detail_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    context = {
        'title': book.title,
        'book': book,
        'categories': Category.objects.all(),
    }
    return render(request, 'book_detail.html', context)


# 4. Про нас
def about_view(request):
    return render(request, 'about.html', {'title': 'Про нас', 'categories': Category.objects.all()})


# 5. Контакти
def contacts_view(request):
    return render(request, 'contacts.html', {'title': 'Контакти', 'categories': Category.objects.all()})