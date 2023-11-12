from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('<slug:genre_slug>/',
         views.BookListView.as_view(),
         name='book_list_by_genre'),
    path('<int:pk>/<slug:slug>/',
         views.BookDetailView.as_view(),
         name='book_detail'),
]

