# Book Review API Project Using Django
This Django project aims to create an API for managing book reviews 
using Django REST Framework and Token Authentication for user authentication.
---
## How to run the project locally:
### 1. Clone the Repository
```bash
git clone https://github.com/ShathaAljuaid1/bookreview.git
cd bookreview 
```
### 2. Create and Activate a Virtual Environment
python -m venv .venv
.venv\Scripts\activate

### 3. Install Requirements
pip install -r requirements.txt

### 4. Apply Migrations
python manage.py migrate

### 5. Run the Local Server
python manage.py runserver

## How to test each endpoint using Postman
### Authentication & User Management
POST /register/
→ Register a new user by providing username, email, and password.

POST /login/
→ Login with credentials and receive a Token.

POST /logout/
→ Logout the user by invalidating the token (optional behavior depending on implementation).

POST /change-password/
→ Authenticated users can change their password by providing the old and new passwords.

### Books
GET /books/
→ List all books. (Accessible to all users)

POST /books/
→ Add a new book. (Admin only)

GET /books/<int:pk>/
→ Retrieve a single book's details.

PUT /books/<int:pk>/
→ Update a book’s data. (Admin only)

DELETE /books/<int:pk>/
→ Delete a book. (Admin only)

### Reviews
GET /books/<int:book_id>/reviews/
→ Get all reviews related to a specific book.

POST /books/<int:book_id>/reviews/
→ Add a review for a specific book. (Authenticated users only)

GET /reviews/<int:review_id>/
→ Retrieve details of a specific review.

PUT /reviews/<int:review_id>/
→ Update a specific review. (Only the review's author)

DELETE /reviews/<int:review_id>/
→ Delete a specific review. (Only the review's author)

## Authentication
This project uses Token Authentication to protect API endpoints and authenticate users.
Login to obtain an authentication token:

Method: POST
Endpoint: /api/login/
Required Content: You must send the username and password in the request body (usually as JSON).