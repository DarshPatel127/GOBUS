from django.urls import path
from .views import PostListView, edit_passenger_details
from .views import PostDetailView, search_results,book,booking_panel, cancel_booking, add_passenger_details
from . import views

from users import views as user_views

urlpatterns = [
    path('', PostListView.as_view(), name='EXP HOME'),
    path('search/', search_results, name='search_results'),
    path('book/<int:bus_id>/', book, name='booking_page'),
    path('view_bookings/',booking_panel,name='view_bookings'),
    path('cancel-booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path('passengers/<int:booking_id>/', add_passenger_details, name='passengers'),
    path('edit_passengers/<int:booking_id>/', edit_passenger_details, name='edit_passengers'),
]

