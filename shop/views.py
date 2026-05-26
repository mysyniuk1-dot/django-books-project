from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from shop.models import Category, Book, Review, ReadingProgress
from shop.forms import ReviewForm, NewsletterForm


# 1. Головна сторінка зі списком книг та формою підписки
def index_view(request):
    books = Book.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():  # <-- Виправлено синтаксис тут!
            newsletter_form.save()
            return redirect('index')
    else:
        newsletter_form = NewsletterForm()

    return render(request, 'index.html', {
        'books': books,
        'categories': categories,
        'newsletter_form': newsletter_form
    })


# 2. Сторінка "Про нас"
def about_view(request):
    categories = Category.objects.all()
    newsletter_form = NewsletterForm()
    return render(request, 'about.html', {
        'categories': categories,
        'newsletter_form': newsletter_form
    })


# 3. Сторінка "Контакти"
def contacts_view(request):
    categories = Category.objects.all()
    newsletter_form = NewsletterForm()
    return render(request, 'contacts.html', {
        'categories': categories,
        'newsletter_form': newsletter_form
    })


# 4. Сторінка книг конкретного жанру
def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    books = category.books.all()
    categories = Category.objects.all()
    newsletter_form = NewsletterForm()
    return render(request, 'category.html', {
        'category': category,
        'books': books,
        'categories': categories,
        'newsletter_form': newsletter_form
    })


# 5. Детальна сторінка книги (з відгуками, формою оцінки та середнім балом)
def book_detail_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    categories = Category.objects.all()
    book_reviews = book.reviews.all()

    # Рахуємо середню оцінку
    avg_rating_data = book_reviews.aggregate(rating_avg=Avg('rating'))
    average_rating = avg_rating_data['rating_avg']
    if average_rating:
        average_rating = round(average_rating, 1)
    else:
        average_rating = "Немає оцінок"

    # Перевіряємо, чи книга вже додана в трекер поточного користувача
    user_progress = None
    if request.user.is_authenticated:
        user_progress = ReadingProgress.objects.filter(user=request.user, book=book).first()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('admin:index')
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = ReviewForm()

    return render(request, 'book_detail.html', {
        'book': book,
        'categories': categories,
        'reviews': book_reviews,
        'average_rating': average_rating,
        'form': form,
        'user_progress': user_progress,
        'newsletter_form': NewsletterForm()
    })


# 6. Додавання/Оновлення книги в трекері читання (Кошик)
@login_required
def add_to_tracker_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        status = request.POST.get('status', 'plan')
        progress, created = ReadingProgress.objects.get_or_create(
            user=request.user,
            book=book,
            defaults={'status': status}
        )
        if not created:
            progress.status = status
            progress.save()

    return redirect('book_detail', book_id=book.id)


# 7. Сторінка перегляду особистого трекера
@login_required
def user_tracker_view(request):
    my_progress = ReadingProgress.objects.filter(user=request.user).select_related('book')
    categories = Category.objects.all()

    return render(request, 'tracker_cart.html', {
        'my_progress': my_progress,
        'categories': categories,
        'newsletter_form': NewsletterForm()
    })