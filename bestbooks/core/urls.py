from django.urls import path
from . import views
# bestbooks/core/urls.py

# Add your URL patterns here, for example:
    # path('', views.home, name='home'),

urlpatterns = [
    path('core/signup/', views.signup_view, name='signup'),
    path('core/login/', views.login_view, name='login'),
    path('core/reset_password/', views.reset_password_view, name='reset_password'),
    path('core/home/', views.home_view, name='home'),  # Assuming you have a home view
    path('core/books/', views.books_view, name='books'),  # Example for a books view
    path('core/profile/<int:id>/', views.profile_view, name='profile'),  # Example for a profile view
    path('core/upload_book/', views.upload_book_view, name='upload_book'),  # Example for uploading a book
]