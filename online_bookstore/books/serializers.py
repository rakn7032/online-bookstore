from rest_framework import serializers
from .models import Book
from datetime import datetime
import ipdb
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'published_date', 'price']

    def to_internal_value(self, data):
        # ipdb.set_trace()
        instance = self.instance
        required_fields = ["title", "author", "description", "published_date", "price"]
        if "book_id" in data.keys():
            required_fields.append("book_id")
            keys_len = 6
        else:
            keys_len = 5

        if not (type(data)==dict and len(data.keys())==keys_len and all(key in data for key in required_fields)):
            raise serializers.ValidationError({"message": "Invalid request data."})
        
        title, author, description = data.get("title"), data.get("author"), data.get("description")
        published_date, price = data.get("published_date"), data.get("price")
        if not(title and type(title)==str and author and type(author)==str and (type(price) in (int, float))):
            raise serializers.ValidationError({"message": "Invalid or missing request data."})
        if (description and (type(description) not in (str, type(None)))) or (published_date and (type(published_date) not in (str, type(None)))):
            raise serializers.ValidationError({"message": "Invalid or missing request data."})
        try:
            datetime.strptime(published_date, '%Y-%m-%d')
        except ValueError:
            raise serializers.ValidationError({"message": "Invalid published date; it must be in the format YYYY-MM-DD and be a valid date."})
        
        if instance:
            if Book.objects.filter(title__iexact=title, author__iexact=author).exclude(id=instance.id).exists():
                raise serializers.ValidationError({"message":"A book with this title and author already exists."})
        else:
            if Book.objects.filter(title__iexact=title, author__iexact=data['author']).exists():
                raise serializers.ValidationError({"message": "A book with this title and author already exists."})

        return super().to_internal_value(data)

    def create(self, validated_data):
        return Book.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.description = validated_data.get('description', instance.description)
        instance.published_date = validated_data.get('published_date', instance.published_date)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance
