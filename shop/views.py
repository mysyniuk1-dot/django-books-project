from django.shortcuts import render

def index_view(request):
    context = {
        'title': 'Головна сторінка книги',
        'heading': 'Вітаємо на платформі книжкових відгуків!',
        'welcome_text': 'Тут ви можете відстежувати свій прогрес читання та ділитися враженнями.'
    }
    return render(request, 'index.html', context)

def about_view(request):
    context = {
        'title': 'Про нас',
        'heading': 'Про наш проєкт',
        'description': 'Цей сайт створено для того, щоб об’єднувати любителів читання та допомагати вести трекінг улюблених книг.'
    }
    return render(request, 'about.html', context)

def contacts_view(request):
    context = {
        'title': 'Контакти',
        'heading': 'Зворотній зв’язок',
        'phone': '+380 99 123 45 67',
        'email': 'support@booktrack.com'
    }
    return render(request, 'contacts.html', context)