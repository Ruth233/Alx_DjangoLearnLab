from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from .views import login_view, logout_view, register_view
from .views import list_books      #required exact line
from .views import LibraryDetailView   # import class-based view separatel

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    # Auth routes
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
]
