from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Movies
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    
    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:movie_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:movie_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/place-order/', views.place_order, name='place_order'),
    
    # Orders
    path('orders/', views.orders_view, name='orders'),
    
    # Reviews
    path('movies/<int:movie_id>/review/', views.create_review, name='create_review'),
    path('reviews/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('reviews/<int:review_id>/update/', views.update_review, name='update_review'),
    path('reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('reviews/<int:review_id>/report/', views.report_review, name='report_review'),
<<<<<<< HEAD

    # Popularity
    path('popularity/', views.popularity_map, name='popularity_map'),
    path('api/trending/<str:region>/', views.api_trending_by_region, name='api_trending_by_region'),
=======
    
    # Ratings
    path('movies/<int:movie_id>/rate/', views.submit_rating, name='submit_rating'),
>>>>>>> c9665a95937983e9b3e9690c62447c3ea61d3def
]
