from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookConfigurations.as_view(http_method_names=['get']), name='book-detail'),
    path('books/<int:id>/', views.BookConfigurations.as_view(http_method_names=['get']), name='book-detail'),
    path('books/create_book', views.BookConfigurations.as_view(http_method_names=['post']), name='book-detail'),
    path('books/update_book', views.BookConfigurations.as_view(http_method_names=['put']), name='book-detail'),
    path('books/delete/<int:id>', views.BookConfigurations.as_view(http_method_names=['delete']), name='book-detail'),
    
]

