# Business Directory API

A Django REST Framework-based business directory API that allows users to browse listings, submit new businesses, and interact with reviews and comments.

---

## 🚀 Features

### 📋 Core Features
- **Public Business Listings** – Browse active business listings with detailed information
- **Business Submissions** – Submit new businesses for review and approval
- **Category System** – Organized business categories with parent-child relationships
- **Review System** – Users can leave reviews and comments on business listings
- **Admin Management** – Comprehensive admin interface for managing submissions, listings, and categories
- **User Authentication** – Registration and login system with token-based authentication
- **Geolocation Support** – Address management with latitude/longitude coordinates

---

## 🏗️ Models

### Core Models
- **User** – Custom user model with admin privileges support
- **Category** – Business categories with hierarchical structure
- **Listing** – Published business listings
- **Submission** – Business submission requests awaiting approval
- **Address** – Geolocation data for listings and submissions
- **Review** – User reviews for business listings
- **Comment** – Comments on reviews

---

## 🔌 API Endpoints

### Public Endpoints
 ```bash
GET    /api/listings/                    # List all active business listings
GET    /api/listings/{id}/              # Retrieve specific listing
POST   /api/submissions/                # Submit new business for approval
GET    /api/categories/                 # List all categories
GET    /api/categories/{id}/            # Retrieve specific category
GET    /api/listings/{id}/reviews/      # Get reviews for a listing
POST   /api/listings/{id}/reviews/      # Create review (authenticated)
GET    /api/listings/{id}/reviews/{id}/ # Get specific review
GET    /api/reviews/{id}/comments/      # Get comments for a review
POST   /api/reviews/{id}/comments/      # Create comment (authenticated)
POST   /api/register/                   # User registration
POST   /api/login/                      # User login
 ```
### Admin Endpoints
 ```bash
GET /api/admin/submissions/ # List all submissions
POST /api/admin/submissions/ # Create submission (admin)
GET /api/admin/submissions/{id}/ # Retrieve submission
PUT /api/admin/submissions/{id}/ # Update submission
POST /api/admin/submissions/{id}/approve/ # Approve and publish submission
POST /api/admin/submissions/{id}/reject/ # Reject submission
GET /api/admin/listings/ # Manage all listings
GET /api/admin/categories/ # Manage categories

 ```

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd business-directory
    ```
2. **Install dependencies**

 ```bash
pip install -r requirements.txt
 ```
3. **Run migrations**
 ```bash
python manage.py migrate
 ```
4. **Create a superuser**

 ```bash
python manage.py createsuperuser
 ```
5. **Run the development server**

 ```bash
python manage.py runserver
 ```

## ⚙️ Configuration

### Django Settings
Add to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_nested',
    'directory',
]
```
### User Registration
```python
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "securepassword"}'
```
### User
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "securepassword"}'
```
### Submit a Business
```bash
curl -X POST http://localhost:8000/api/submissions/ \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Test Business",
    "description": "A great test business",
    "contact_email": "business@example.com",
    "phone_number": "+1234567890",
    "website_url": "https://example.com",
    "category": 1,
    "address": {
      "street": "123 Test St",
      "city": "Test City",
      "province_state": "Test State",
      "country": "Test Country"
    }
  }'
```
#### Browse Listings
```bash
curl http://localhost:8000/api/listings/
```

### 🛠️ Admin Interface

Access the Django admin interface at `/admin/` to manage:

- **User accounts and permissions**
- **Business categories and hierarchy**
- **Listing submissions and approvals**
- **Published business listings**
- **User reviews and comments**
### Admin Features
- **Submission Management** – Approve or reject business submissions with bulk actions
- **Listing Management** – Activate/deactivate listings and update business information
- **Category Management** – Create and organize business categories
- **User Management** – Manage user accounts and admin privileges

## 🧪 Testing

Run the test suite:
```bash
python manage.py test directory
```

## 🔐 Permissions

The API implements several permission classes:

- **IsAdminOrReadOnly** – Read access for all, write access for admins only
- **IsOwnerOrReadOnly** – Users can only modify their own content
- **IsAdminUser** – Admin-only access for sensitive operations
- **IsAuthenticatedOrReadOnly** – Authenticated users can write, anyone can read

  ## 🏗️ Development

### Adding New Features
1. **Create model migrations**
   ```bash
   python manage.py makemigrations
   ```
2. **Update serializers** in `serializers.py`
3. **Add views** in `views.py`
4. **Configure URLs** in `urls.py`
5. **Update admin interface** in `admin.py`

### Code Structure
- **models.py** – Database models and relationships
- **serializers.py** – API serializers for data transformation
- **views.py** – API endpoints and business logic
- **urls.py** – URL routing and nested routes
- **admin.py** – Django admin configuration
- **permissions.py** – Custom permission classes
