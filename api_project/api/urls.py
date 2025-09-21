from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookList, BookViewSet



# Create the router and register the ViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
     path('token/', obtain_auth_token, name='api-token'),   # ✅ new endpoint to get tokens
    #  Include all CRUD routes from the router
    path('', include(router.urls)),
    
]
