from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Book
from .serializers import BookSerializer
from authentication.views import has_permission

class BookConfigurations(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        required_permissions = ["view_books"]
        has_perm, message = has_permission(request.user, required_permissions)
        if not has_perm: return Response({'message': message, "status": False}, status=status.HTTP_403_FORBIDDEN)

        if id:
            book = Book.objects.filter(id=id).first()
            if not book:
                return Response({"message":"No Book matches the given id.", "status":False}, status=status.HTTP_400_BAD_REQUEST)
            serializer = BookSerializer(book)
        else:
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK) 
    
    def post(self, request):
        required_permissions = ["create_book"]
        has_perm, message = has_permission(request.user, required_permissions)
        if not has_perm: return Response({'message': message, "status": False}, status=status.HTTP_403_FORBIDDEN)

        serializer = BookSerializer(data=request.data)
        
        if serializer.is_valid():
            book = serializer.save()
            return Response({"message": "Book created successfully", "data": serializer.data, 'status': True}, status=status.HTTP_201_CREATED)
        
        invalid = serializer.errors
        invalid["status"] = False
        return Response(invalid, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        required_permissions = ["update_book"]
        has_perm, message = has_permission(request.user, required_permissions)
        if not has_perm: return Response({'message': message, "status": False}, status=status.HTTP_403_FORBIDDEN)
        
        book_id = request.data.get('book_id')
        if not (book_id and type(book_id)==int):
            return Response({"message": "Book ID is required.", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        book = Book.objects.filter(id=book_id).first()
        if not book:
            return Response({"message": "Book not found.", "status": False}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Book updated successfully.", "user": serializer.data}, status=status.HTTP_200_OK)
        
        invalid = serializer.errors
        invalid["status"] = False
        return Response(invalid, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        required_permissions = ["delete_book"]
        has_perm, message = has_permission(request.user, required_permissions)
        if not has_perm: return Response({'message': message, "status": False}, status=status.HTTP_403_FORBIDDEN)

        if not id:
            return Response({"message":"Book ID is required.", "status":False}, status=status.HTTP_400_BAD_REQUEST)
        book = Book.objects.filter(id=id).first()
        if not book:
            return Response({"message":"No Book matches the given id.", "status":False}, status=status.HTTP_400_BAD_REQUEST)

        book.delete()
        return Response({"message":"Book deleted succesfully.", "status":True}, status=status.HTTP_200_OK)