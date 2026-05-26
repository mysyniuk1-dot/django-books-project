from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Нова таблиця: Категорії (Жанри)
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва жанру")
    description = models.TextField(verbose_name="Опис жанру", blank=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанри"

    def __str__(self):
        return self.name


# Оновлена таблиця: Книги
class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="books", verbose_name="Жанр")
    title = models.CharField(max_length=200, verbose_name="Назва книги")
    author = models.CharField(max_length=150, verbose_name="Автор")
    description = models.TextField(verbose_name="Опис книги", blank=True)
    # Поле для обкладинки книги
    image = models.ImageField(upload_to='books_covers/', blank=True, null=True, verbose_name="Обкладинка книги")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return f"{self.title} — {self.author}"


# Таблиця відгуків
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews", verbose_name="Книга")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    text = models.TextField(verbose_name="Текст відгуку")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Оцінка (1-5)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"

    def __str__(self):
        return f"Відгук від {self.user.username} на книгу {self.book.title}"


# Таблиця прогресу читання
class ReadingProgress(models.Model):
    STATUS_CHOICES = [('plan', 'Планую прочитати'), ('reading', 'Читаю зараз'), ('read', 'Прочитано')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='plan', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    class Meta:
        verbose_name = "Прогрес читання"
        verbose_name_plural = "Прогрес читання"
        unique_together = ('user', 'book')

    def __str__(self):
        status_display = getattr(self, 'get_status_display')()
        return f"{self.user.username} - {self.book.title} ({status_display})"