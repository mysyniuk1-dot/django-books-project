from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect

from shop.forms import ReviewForm, NewsletterForm, UserRegisterForm
from shop.models import Category, Book, ReadingProgress


def index_view(request):
    books = Book.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            newsletter_form.save()
            return redirect('index')
    else:
        newsletter_form = NewsletterForm()
    return render(request, 'index.html', {'books': books, 'categories': categories, 'newsletter_form': newsletter_form})


def about_view(request):
    return render(request, 'about.html', {'categories': Category.objects.all(), 'newsletter_form': NewsletterForm()})


def contacts_view(request):
    return render(request, 'contacts.html', {'categories': Category.objects.all(), 'newsletter_form': NewsletterForm()})


def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'category.html', {
        'category': category,
        'books': category.books.all(),
        'categories': Category.objects.all(),
        'newsletter_form': NewsletterForm()
    })


def book_detail_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book_reviews = book.reviews.all()

    avg_rating_data = book_reviews.aggregate(rating_avg=Avg('rating'))
    average_rating = round(avg_rating_data['rating_avg'], 1) if avg_rating_data['rating_avg'] else "Немає оцінок"

    user_progress = None
    if request.user.is_authenticated:
        user_progress = ReadingProgress.objects.filter(user=request.user, book=book).first()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
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
        'categories': Category.objects.all(),
        'reviews': book_reviews,
        'average_rating': average_rating,
        'form': form,
        'user_progress': user_progress,
        'newsletter_form': NewsletterForm()
    })


# ДОДАВАННЯ ДО КОШИКА
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
    return redirect('user_tracker')


# СТОРІНКА ПЕРЕГЛЯДУ КОШИКА
@login_required
def user_tracker_view(request):
    my_progress = ReadingProgress.objects.filter(user=request.user).select_related('book')
    return render(request, 'tracker_cart.html', {
        'my_progress': my_progress,
        'categories': Category.objects.all(),
        'newsletter_form': NewsletterForm()
    })


# ЛАБА 8: АВТЕНТИФІКАЦІЯ
def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html',
                  {'form': form, 'categories': Category.objects.all(), 'newsletter_form': NewsletterForm()})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html',
                  {'form': form, 'categories': Category.objects.all(), 'newsletter_form': NewsletterForm()})


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def profile_view(request):
    if request.user.is_staff:
        orders = ReadingProgress.objects.all().select_related('user', 'book')
    else:
        orders = ReadingProgress.objects.filter(user=request.user).select_related('book')

    return render(request, 'registration/profile.html', {
        'orders': orders,
        'categories': Category.objects.all(),
        'newsletter_form': NewsletterForm()
    })