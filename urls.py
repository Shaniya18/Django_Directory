from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import (
    ListingViewSet,
    SubmissionViewSet,
    SubmissionAdminViewSet,
    CategoryViewSet,
    ListingAdminViewSet,
    CategoryAdminViewSet,
    ReviewViewSet,
    CommentViewSet,
    UserRegistrationView,
    LoginView,
)

# Create a root router for the public-facing API endpoints.
router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'submissions', SubmissionViewSet, basename='submission')
router.register(r'categories', CategoryViewSet, basename='category')

# Create a nested router for reviews and comments.
# This creates a structure like: /listings/{listing_pk}/reviews/
listings_router = routers.NestedSimpleRouter(router, r'listings', lookup='listing')
listings_router.register(r'reviews', ReviewViewSet, basename='listing-reviews')

# This creates a structure like: /reviews/{review_pk}/comments/
reviews_router = routers.NestedSimpleRouter(listings_router, r'reviews', lookup='review')
reviews_router.register(r'comments', CommentViewSet, basename='review-comments')

# Create a separate router for admin-only endpoints.
# These routes are for a future authenticated admin panel.
admin_router = DefaultRouter()
admin_router.register(r'submissions', SubmissionAdminViewSet, basename='admin-submission')
admin_router.register(r'listings', ListingAdminViewSet, basename='admin-listing')
admin_router.register(r'categories', CategoryAdminViewSet, basename='admin-category')

urlpatterns = [
    # Include all public API endpoints.
    path('api/', include(router.urls)),
    path('api/', include(listings_router.urls)),
    path('api/', include(reviews_router.urls)),

    # Include admin-only endpoints.
    path('api/admin/', include(admin_router.urls)),

    # Authentication and user registration endpoints.
    path('api/register/', UserRegistrationView.as_view(), name='user-register'),
    path('api/login/', LoginView.as_view(), name='user-login'),
]
