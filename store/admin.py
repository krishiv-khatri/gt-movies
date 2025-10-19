from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Movie, Review, Cart, Order, OrderItem, Rating


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'rating', 'release_year', 'price', 'created_at']
    list_filter = ['genre', 'rating', 'release_year', 'created_at', 'price']
    search_fields = ['title', 'description', 'director', 'cast']
    ordering = ['-created_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'image', 'price')
        }),
        ('Movie Details', {
            'fields': ('genre', 'rating', 'director', 'cast', 'release_year', 'duration', 'language')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'movie__title']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'movie__title', 'content']
    ordering = ['-created_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_movie_count', 'get_total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']
    ordering = ['-created_at']
    
    def get_movie_count(self, obj):
        return obj.get_movie_count()
    get_movie_count.short_description = 'Movie Count'
    
    def get_total_price(self, obj):
        return f"${obj.get_total_price():.2f}"
    get_total_price.short_description = 'Total Price'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'get_total_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username']
    ordering = ['-created_at']
    inlines = [OrderItemInline]
    
    def get_total_price(self, obj):
        return f"${obj.get_total_price():.2f}"
    get_total_price.short_description = 'Total Price'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'movie', 'quantity', 'price', 'get_total_price']
    list_filter = ['order__status', 'order__created_at']
    search_fields = ['order__user__username', 'movie__title']
    ordering = ['-order__created_at']
    
    def get_total_price(self, obj):
        return f"${obj.get_total_price():.2f}"
    get_total_price.short_description = 'Total Price'


# Customize User admin
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email']


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
