from django.urls import path
from .views import edit_passenger_details
from .views import home, search_results,book,booking_panel, cancel_booking
from . import views

from users import views as user_views

urlpatterns = [
    path('', home, name='EXP HOME'),
    path('search/', search_results, name='search_results'),
    path('book/<int:bus_id>/', book, name='booking_page'),
    path('view_bookings/',booking_panel,name='view_bookings'),
    path('cancel-booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    #path('passengers/<int:booking_id>/', book, name='passengers'),
    path('edit_passengers/<int:booking_id>/', edit_passenger_details, name='edit_passengers'),
]

