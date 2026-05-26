from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from shop.views import index_view, about_view, contacts_view, category_view, book_detail_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('about/', about_view, name='about'),
    path('contacts/', contacts_view, name='contacts'),
    path('category/<int:category_id>/', category_view, name='category'),
    path('book/<int:book_id>/', book_detail_view, name='book_detail'),
]

# Дозволяємо роботу з медіафайлами (картинками) під час розробки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)