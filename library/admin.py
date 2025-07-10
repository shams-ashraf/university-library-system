from django.contrib import admin 
from .models import Book, Borrowed, userProfile

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'isbn', 
        'title', 
        'author', 
        'published_year', 
        'publisher', 
        'quantity', 
        'category'
    )

@admin.register(Borrowed)
class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = (
        'borrower_name', 
        'telephone', 
        'national_id', 
        'isbn', 
        'start_date', 
        'due_date', 
        'user_email',  
        'remaining_days'
    )

    @admin.display(description='Email')
    def user_email(self, obj):
        return obj.user.email if obj.user else 'N/A'

@admin.register(userProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'is_admin',
        'phone_number',
        'city',
        'country'
    )
