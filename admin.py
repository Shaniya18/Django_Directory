from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Category, Listing, Review, Submission, User, Address, Comment

# Create a custom Admin class for the User model.
class UserAdmin(BaseUserAdmin):
    """
    Custom Admin interface for the User model.
    """
    list_display = ('username', 'email', 'is_staff', 'is_admin', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom fields', {'fields': ('is_admin',)}),
    )

class SubmissionAdmin(admin.ModelAdmin):
    """
    Custom Admin interface for the Submission model.
    """
    list_display = ('business_name', 'contact_email', 'category', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('business_name', 'contact_email')
    actions = ['approve_submissions', 'reject_submissions']

    @admin.action(description='Mark selected submissions as approved')
    def approve_submissions(self, request, queryset):
        # Your approval logic here, maybe trigger a view function or a service
        # For simplicity, we just change the status
        queryset.update(status='approved')
        self.message_user(request, "Selected submissions have been approved.")

    @admin.action(description='Mark selected submissions as rejected')
    def reject_submissions(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, "Selected submissions have been rejected.")

class ListingAdmin(admin.ModelAdmin):
    """
    Custom Admin interface for the Listing model.
    """
    list_display = ('business_name', 'category', 'is_active', 'created_at')
    list_filter = ('is_active', 'category')
    search_fields = ('business_name', 'description')
    
class CategoryAdmin(admin.ModelAdmin):
    """
    Custom Admin interface for the Category model.
    """
    list_display = ('name', 'parent_category')
    search_fields = ('name',)

class ReviewAdmin(admin.ModelAdmin):
    """
    Custom Admin interface for the Review model.
    """
    list_display = ('listing', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('comment', 'user__username', 'listing__business_name')
    
class CommentAdmin(admin.ModelAdmin):
    """
    Custom Admin interface for the Comment model.
    """
    list_display = ('review', 'user', 'created_at')
    search_fields = ('text', 'user__username')

class AddressAdmin(admin.ModelAdmin):
    """
    Custom Admin interface for the Address model.
    """
    list_display = ('street', 'city', 'country')
    search_fields = ('street', 'city', 'country')

# Register your models with the custom admin classes.
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Address, AddressAdmin)
