from django.shortcuts import render
from shop.models import Book  # Імпортуємо модель книг


def index_view(request):
    # Витягуємо всі книги, які ви додали через адмінку
    books_from_db = Book.objects.all()

    context = {
        'title': 'Головна — Список книг',
        'heading': 'Каталог книг вашої бібліотеки',
        'books': books_from_db  # Передаємо список книг у шаблон
    }
    return render(request, 'index.html', context)


def about_view(request):
    return render(request, 'about.html', {'title': 'Про нас'})


def contacts_view(request):
    context = {
        'title': 'Контакти',
        'phone': '+380 (99) 123-45-67',
        'email': 'support@booktracking.local'
    }
    return render(request, 'contacts.html', context)