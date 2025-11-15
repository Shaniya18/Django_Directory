from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    # Add unique related_name to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name='directory_user_groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='directory_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Address(models.Model):
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    province_state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    # The address is linked to either a Listing or a Submission.
    listing = models.OneToOneField('Listing', on_delete=models.CASCADE, null=True, blank=True, related_name='address_listing')
    submission_address = models.OneToOneField('Submission', on_delete=models.CASCADE, null=True, blank=True, related_name='address_submission')
    
    def __str__(self):
        return f"{self.street}, {self.city}"

class Listing(models.Model):
    business_name = models.CharField(max_length=255)
    description = models.TextField()
    contact_email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    website_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listings')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.business_name

class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviews')

    def __str__(self):
        return f"Review for {self.listing.business_name}"

class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')

    def __str__(self):
        return f"Comment on {self.review.listing.business_name} review"

class Submission(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    business_name = models.CharField(max_length=255)
    description = models.TextField()
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)
    website_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name
