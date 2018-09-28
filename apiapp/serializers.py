from rest_framework import serializers
from mainapp.models import Author, Book, Tag, URL_DICT

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


SRLZR_DICT = {Author.Other.url:AuthorSerializer,
            Book.Other.url:BookSerializer,
            Tag.Other.url:TagSerializer,
            }