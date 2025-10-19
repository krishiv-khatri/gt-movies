from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg, Sum
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Order, OrderItem

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
    reviews = movie.reviews.filter(is_reported=False)  # Only show non-reported reviews
    
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
@login_required
def place_order(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.movies.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    # 👇 get region directly from the user record
    region = getattr(request.user, "region", "southeast")

    order = Order.objects.create(
        user=request.user,
        status='pending',
        region=region     # 👈 stores the user’s region on every order
    )

    for movie in cart.movies.all():
        OrderItem.objects.create(order=order, movie=movie, quantity=1, price=movie.price)

    cart.movies.clear()
    messages.success(request, f"Order #{order.id} placed successfully!")
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


@login_required
@require_POST
def report_review(request, review_id):
    """Report a review as inappropriate"""
    review = get_object_or_404(Review, id=review_id)
    
    # Prevent users from reporting their own reviews
    if review.user == request.user:
        return JsonResponse({
            'success': False, 
            'message': 'You cannot report your own review.'
        })
    
    # Check if review is already reported
    if review.is_reported:
        return JsonResponse({
            'success': False, 
            'message': 'This review has already been reported.'
        })
    
    # Mark review as reported
    review.is_reported = True
    review.save()
    
    return JsonResponse({
        'success': True, 
        'message': 'Review reported successfully. It has been removed from the page.'
    })

    # Page: renders the map
def popularity_map(request):
    regions = dict(Order.REGION_CHOICES)
    return render(request, 'store/popularity_map.html', {'regions': regions})


def api_trending_by_region(request, region):
    """Returns top movies by region, or global if region='global'."""
    valid_regions = {k for k, _ in Order.REGION_CHOICES}

    # Debug log (appears in console)
    print(f"DEBUG: Requested region = {region}")

    # ✅ Handle the global case first
    if region == "global":
        qs = (OrderItem.objects
              .values('movie__title')
              .annotate(total=Sum('quantity'))
              .order_by('-total')[:10])
        print("DEBUG: Using GLOBAL query")
    elif region in valid_regions:
        qs = (OrderItem.objects
              .filter(order__region=region)
              .values('movie__title')
              .annotate(total=Sum('quantity'))
              .order_by('-total')[:10])
        print(f"DEBUG: Using REGION query: {region}")
    else:
        print("DEBUG: INVALID region triggered")
        return JsonResponse({'error': f'invalid region: {region}'}, status=400)

    data = [{'title': row['movie__title'], 'count': row['total']} for row in qs]
    print(f"DEBUG: Returned {len(data)} movies")
    return JsonResponse({'region': region, 'top': data})
