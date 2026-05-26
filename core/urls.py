from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name='index'),
    path('about/', views.about_view, name='about'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('category/<int:category_id>/', views.category_view, name='category'),
    path('book/<int:book_id>/', views.book_detail_view, name='book_detail'),

    # КОРУВАННЯ КОШИКОМ
    path('book/<int:book_id>/add-to-tracker/', views.add_to_tracker_view, name='add_to_tracker'),
    path('tracker/', views.user_tracker_view, name='user_tracker'),

    # АВТОРИЗАЦІЯ ТА КАБІНЕТ (Лаба 8)
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # ВІДНОВЛЕННЯ ПАРОЛЯ ЧЕРЕЗ EMAIL (Лаба 8)
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)