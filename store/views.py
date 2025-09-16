from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Movie, Review, Cart, Order, OrderItem
from .forms import CustomUserCreationForm, ReviewForm, MovieSearchForm


def home(request):
    """Home page with app information"""
    featured_movies = Movie.objects.all()[:6]  # Show 6 featured movies
    return render(request, 'store/home.html', {'featured_movies': featured_movies})


def register_view(request):
    """User registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a cart for the new user
            Cart.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    """User login"""
    if request.method == 'POST':
        from django.contrib.auth import authenticate
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'store/login.html')


def logout_view(request):
    """User logout"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


def movie_list(request):
    """List all movies with search functionality"""
    movies = Movie.objects.all()
    search_form = MovieSearchForm(request.GET)
    
    if search_form.is_valid() and search_form.cleaned_data['search']:
        search_query = search_form.cleaned_data['search']
        movies = movies.filter(title__icontains=search_query)
    
    # Add average rating to each movie
    for movie in movies:
        movie.avg_rating = movie.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    
    paginator = Paginator(movies, 12)  # Show 12 movies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'store/movie_list.html', {
        'page_obj': page_obj,
        'search_form': search_form,
    })


def movie_detail(request, movie_id):
    """Movie details and reviews"""
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = movie.reviews.all()
    
    # Calculate average rating
    avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    
    # Check if user has already reviewed this movie
    user_review = None
    if request.user.is_authenticated:
        try:
            user_review = reviews.get(user=request.user)
        except Review.DoesNotExist:
            pass
    
    # Review form
    review_form = ReviewForm()
    
    return render(request, 'store/movie_detail.html', {
        'movie': movie,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'user_review': user_review,
        'review_form': review_form,
    })


@login_required
def cart_view(request):
    """View shopping cart"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart})


@login_required
@require_POST
def add_to_cart(request, movie_id):
    """Add movie to cart"""
    movie = get_object_or_404(Movie, id=movie_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if movie not in cart.movies.all():
        cart.movies.add(movie)
        messages.success(request, f'{movie.title} added to cart!')
    else:
        messages.info(request, f'{movie.title} is already in your cart!')
    
    return redirect('movie_detail', movie_id=movie_id)


@login_required
@require_POST
def remove_from_cart(request, movie_id):
    """Remove movie from cart"""
    movie = get_object_or_404(Movie, id=movie_id)
    cart = get_object_or_404(Cart, user=request.user)
    
    if movie in cart.movies.all():
        cart.movies.remove(movie)
        messages.success(request, f'{movie.title} removed from cart!')
    
    return redirect('cart')


@login_required
@require_POST
def clear_cart(request):
    """Remove all items from cart"""
    cart = get_object_or_404(Cart, user=request.user)
    cart.movies.clear()
    messages.success(request, 'Cart cleared!')
    return redirect('cart')


@login_required
def orders_view(request):
    """View order history"""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/orders.html', {'orders': orders})


@login_required
@require_POST
def place_order(request):
    """Place order from cart"""
    cart = get_object_or_404(Cart, user=request.user)
    
    if not cart.movies.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('cart')
    
    # Create order
    order = Order.objects.create(user=request.user)
    
    # Add movies to order
    for movie in cart.movies.all():
        OrderItem.objects.create(
            order=order,
            movie=movie,
            quantity=1,
            price=movie.price
        )
    
    # Clear cart
    cart.movies.clear()
    
    messages.success(request, f'Order #{order.id} placed successfully!')
    return redirect('orders')


@login_required
@require_POST
def create_review(request, movie_id):
    """Create a new review"""
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Check if user already reviewed this movie
    if Review.objects.filter(movie=movie, user=request.user).exists():
        messages.error(request, 'You have already reviewed this movie!')
        return redirect('movie_detail', movie_id=movie_id)
    
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.movie = movie
        review.user = request.user
        review.save()
        messages.success(request, 'Review created successfully!')
    else:
        messages.error(request, 'Please correct the errors below.')
    
    return redirect('movie_detail', movie_id=movie_id)


@login_required
def edit_review(request, review_id):
    """Edit review page"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully!')
            return redirect('movie_detail', movie_id=review.movie.id)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'store/edit_review.html', {
        'form': form,
        'review': review,
    })


@login_required
@require_POST
def update_review(request, review_id):
    """Update an existing review (legacy endpoint)"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    form = ReviewForm(request.POST, instance=review)
    if form.is_valid():
        form.save()
        messages.success(request, 'Review updated successfully!')
    else:
        messages.error(request, 'Please correct the errors below.')
    
    return redirect('movie_detail', movie_id=review.movie.id)


@login_required
@require_POST
def delete_review(request, review_id):
    """Delete a review"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    movie_id = review.movie.id
    review.delete()
    messages.success(request, 'Review deleted successfully!')
    return redirect('movie_detail', movie_id=movie_id)
