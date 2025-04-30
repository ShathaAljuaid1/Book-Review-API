from rest_framework.views import APIView
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer
from rest_framework.permissions import IsAdminUser, AllowAny
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response



# ✅ List all books
class BookListView(APIView):
    # تعيين صلاحيات بناءً على نوع الطلب
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]  # فقط الإداري يقدر يضيف
        return [AllowAny()]  # الكل يقدر يتصفح الكتب

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Get details of a specific book
class BookDetailView(APIView):
    permission_classes = [permissions.AllowAny]  # الجميع يمكنهم مشاهدة تفاصيل الكتب

    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = Book.objects.get(pk=pk)
        if not request.user.is_staff:  # التأكد من أن المستخدم هو إداري
            return Response({"detail": "Only admin users can edit books."}, status=status.HTTP_403_FORBIDDEN)

        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = Book.objects.get(pk=pk)
        if not request.user.is_staff:  # التأكد من أن المستخدم هو إداري
            return Response({"detail": "Only admin users can delete books."}, status=status.HTTP_403_FORBIDDEN)

        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ✅ List or Create Reviews for a Book
class ReviewListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, book_id):
        reviews = Review.objects.filter(book__id=book_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Edit or Delete Own Review
class ReviewDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, review_id):
        review = get_object_or_404(Review, pk=review_id, user=request.user)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id):
        review = get_object_or_404(Review, pk=review_id, user=request.user)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response({"detail": "Both old and new passwords are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({"detail": "Old password is incorrect."},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password changed successfully."})



@api_view(['POST'])
def register_user(request):
   if request.method == 'POST':
       serializer = UserSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
   if request.method == 'POST':
       username = request.data.get('username')
       password = request.data.get('password')

       user = None
       if '@' in username:
           try:
               user = CustomUser.objects.get(email=username)
           except ObjectDoesNotExist:
               pass

       if not user:
           user = authenticate(username=username, password=password)

       if user:
           token, _ = Token.objects.get_or_create(user=user)
           return Response({'token': token.key}, status=status.HTTP_200_OK)

       return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
   if request.method == 'POST':
       try:
           # Delete the user's token to logout
           request.user.auth_token.delete()
           return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
       except Exception as e:
           return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
