from django import forms
from shop.models import Review, NewsletterSubscriber


# Форма оцінки книги (товару)
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f"{i} ★") for i in range(1, 6)],
                attrs={'style': 'padding: 8px; border-radius: 5px; width: 100%; border: 1px solid #ccc;'}
            ),
            'text': forms.Textarea(
                attrs={'rows': 4, 'placeholder': 'Напишіть ваше враження про книгу...', 'style': 'padding: 10px; border-radius: 5px; width: 100%; border: 1px solid #ccc;'}
            )}


# Форма підписки на розсилку
class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(
                attrs={'placeholder': 'Введіть ваш Email...', 'style': 'padding: 10px; border-radius: 5px; border: 1px solid #4b5563; background: #374151; color: white; width: 100%;'}
            )}