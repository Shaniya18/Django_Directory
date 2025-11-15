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
