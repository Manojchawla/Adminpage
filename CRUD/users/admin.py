from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_no')  # Fields to display in the admin panel
    search_fields = ('name', 'email', 'phone_no')  # Enable search
    list_filter = ('name',)  # Add filters
    ordering = ('name',)  # Default ordering
