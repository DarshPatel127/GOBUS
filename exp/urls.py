from django.urls import path
from .views import PostListView
from .views import PostDetailView, search_results,book
from . import views

from users import views as user_views

urlpatterns = [
    path('', PostListView.as_view(), name='EXP HOME'),
    path('search/', search_results, name='search_results'),
    path('book/<int:bus_id>/', book, name='booking_page')
]

