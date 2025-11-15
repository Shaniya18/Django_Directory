from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .models import Listing, Submission, Category, Review, Comment, User
from .serializers import (
    ListingSerializer,
    SubmissionSerializer,
    CategorySerializer,
    ReviewSerializer,
    CommentSerializer,
    ListingUpdateSerializer,
    UserSerializer,
    AuthTokenSerializer
)

# A custom view to handle user login and authentication token creation.
class LoginView(ObtainAuthToken):
    """
    API endpoint that allows users to log in and receive an authentication token.
    Uses DRF's built-in token authentication.
    """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserRegistrationView(generics.CreateAPIView):
    """
    API view for user registration.
    Allows new users to create an account.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# ViewSet for public-facing Listing endpoints.
class ListingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows listings to be viewed.
    """
    queryset = Listing.objects.filter(is_active=True).order_by('business_name')
    serializer_class = ListingSerializer
    lookup_field = 'id'

# ViewSet for public-facing Submission endpoints.
class SubmissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows new business submissions to be created.
    """
    queryset = Submission.objects.all().order_by('-created_at')
    serializer_class = SubmissionSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post'] # Only allow POST requests for new submissions

# ViewSet for admin-only management of submissions.
class SubmissionAdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows administrators to manage submissions.
    """
    queryset = Submission.objects.all().order_by('-created_at')
    serializer_class = SubmissionSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Approves a submission and creates a new listing.
        """
        submission = get_object_or_404(Submission, pk=pk)

        with transaction.atomic():
            # Create a new Listing object from the submission data.
            listing_data = {
                'business_name': submission.business_name,
                'description': submission.description,
                'contact_email': submission.contact_email,
                'phone_number': submission.phone_number,
                'website_url': submission.website_url,
                'category': submission.category,
                'submission': submission,
                'is_active': True,
            }
            listing = Listing.objects.create(**listing_data)

            # Retrieve and re-link the address from the submission to the new listing.
            try:
                submission_address = submission.address
                submission_address.listing = listing
                submission_address.submission_address = None # Unlink from submission
                submission_address.save()
            except Address.DoesNotExist:
                pass

            # Update the submission status.
            submission.status = 'approved'
            submission.save()

        return Response({"status": "Submission approved and published.", "listing_id": listing.id})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        Rejects a submission.
        """
        submission = get_object_or_404(Submission, pk=pk)

        # Update the submission status to 'rejected'.
        submission.status = 'rejected'
        submission.save()

        return Response({"status": "Submission rejected."})

# ViewSet for public-facing Category endpoints.
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows categories to be viewed.
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

# ViewSet for admin-only management of categories.
class CategoryAdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint for administrators to manage categories.
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

# ViewSet for admin-only management of listings.
class ListingAdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint for administrators to manage all listings.
    """
    queryset = Listing.objects.all().order_by('business_name')
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        # Use a different serializer for write operations (create, update)
        if self.action in ['create', 'update', 'partial_update']:
            return ListingUpdateSerializer
        return ListingSerializer

# ViewSet for managing reviews on a listing.
class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reviews to be created, viewed, and managed.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

    def get_queryset(self):
        listing_id = self.kwargs.get('listing_id')
        queryset = Review.objects.filter(listing_id=listing_id).order_by('-created_at')
        return queryset

    def perform_create(self, serializer):
        listing = get_object_or_404(Listing, id=self.kwargs.get('listing_id'))
        serializer.save(user=self.request.user, listing=listing)

# ViewSet for managing comments on a review.
class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be created, viewed, and managed.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        queryset = Comment.objects.filter(review_id=review_id).order_by('-created_at')
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(user=self.request.user, review=review)
