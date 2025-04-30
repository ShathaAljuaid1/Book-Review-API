from django.urls import path
from .views import (
    BookListView, BookDetailView, ReviewListCreateView, ReviewDetailView,
    ChangePasswordView, register_user, user_login, user_logout)

urlpatterns = [
    # تسجيل مستخدم جديد
    path('register/', register_user, name='register'),
    # تسجيل الدخول
    path('login/', user_login, name='login'),
    # تسجيل الخروج
    path('logout/', user_logout, name='logout'),
    # تغيير كلمة السر
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    # عرض كل الكتب + إضافة كتاب (admin only)
    path('books/', BookListView.as_view(), name='book-list'),
    # عرض تفاصيل كتاب معين او تعديل + حذف كتاب (admin only)
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    # عرض كل المراجعات لكتاب معين أو إضافة مراجعة
    path('books/<int:book_id>/reviews/', ReviewListCreateView.as_view(), name='book-reviews'),
    # تعديل، حذف مراجعة معينة
    path('reviews/<int:review_id>/', ReviewDetailView.as_view(), name='review-detail'),
]
