from rest_framework import serializers
from .models import Category, Submission, Listing, Address, Review, Comment, User
from django.db import transaction
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# This serializer handles user registration.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_admin']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# This serializer is for user authentication (login).
class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')
        
        data['user'] = user
        return data

# This serializer handles the Address model, nested within the Listing serializer.
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'city', 'province_state', 'country', 'latitude', 'longitude']

# This serializer handles the Category model.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_category']
        depth = 1 # This will automatically include the parent category's details.

# This serializer is used for public submissions. It is a ModelSerializer with
# a custom create method to handle nested data.
class SubmissionSerializer(serializers.ModelSerializer):
    # This nested serializer allows us to handle the Address data within the submission
    address = AddressSerializer(write_only=True)

    class Meta:
        model = Submission
        fields = [
            'id', 'business_name', 'description', 'contact_email', 'phone_number',
            'website_url', 'category', 'created_at', 'address'
        ]
        read_only_fields = ['created_at']

    def create(self, validated_data):
        # We need to handle the nested address data manually.
        with transaction.atomic():
            # Pop the address data so it's not passed to the Submission.objects.create().
            address_data = validated_data.pop('address')
            submission = Submission.objects.create(**validated_data)
            Address.objects.create(submission_address=submission, **address_data)
            return submission

# This serializer handles the Listing model. It includes the Address and Category serializers
# to provide a complete view of a listing as specified in your API documentation.
class ListingSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'business_name', 'description', 'contact_email', 'phone_number',
            'website_url', 'created_at', 'category', 'address'
        ]

# This is a serializer for a POST request to update a listing.
class ListingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            'id', 'business_name', 'description', 'contact_email', 'phone_number',
            'website_url', 'is_active', 'category'
        ]

# This serializer is for creating new reviews.
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'listing', 'rating', 'comment', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']

# This serializer is for creating new comments.
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'review', 'text', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']
