from .models import Book, Review
from rest_framework import serializers
from .models import CustomUser


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # يظهر اسم المستخدم بدل ID
    book = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'book', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at', 'book']


class UserSerializer(serializers.ModelSerializer):
   class Meta:
       model = CustomUser
       fields = ['username', 'email', 'password']
       extra_kwargs = {'password': {'write_only': True}}

   def create(self, validated_data):
       user = CustomUser(
           username=validated_data['username'],
           email=validated_data['email']
       )
       user.set_password(validated_data['password'])
       user.save()
       return user
