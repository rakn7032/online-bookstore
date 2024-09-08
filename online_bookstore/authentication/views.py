from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateUserSerializer, UpdateUserSerializer
from .models import User, UserAuth
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterUser(APIView):
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"message": "User registered successfully.", "user": serializer.data}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"message": "An error occurred while creating the user.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        invalid = serializer.errors
        invalid["status"] = False
        return Response(invalid, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        required_permissions = ["update_user"]
        has_perm, message = has_permission(request.user, required_permissions)
        if not has_perm: return Response({'message': message, "status": False}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"message": "User ID is required.", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({"message": "User not found.", "status": False}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully.", "user": serializer.data}, status=status.HTTP_200_OK)
        
        invalid = serializer.errors
        invalid["status"] = False
        return Response(invalid, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    def get_token(self, user):
        token = RefreshToken.for_user(user)
        token['user_id'] = user.id
        token['admin'] = user.is_admin
        token['permissions'] = self.get_user_permissions(user)
        return token

    def get_user_permissions(self, user):
        try:
            user_auth = UserAuth.objects.get(user=user)
            permissions = user_auth.permissions.all()
            permission_names = [permission.name for permission in permissions]
            return permission_names
        except UserAuth.DoesNotExist:
            return []

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        if not(email and password): return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user: return Response({"message": "Invalid credentials", "status":False}, status=status.HTTP_401_UNAUTHORIZED)
        elif not user.check_password(password): return Response({"message": "Invalid credentials", "status":False}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = self.get_token(user)
        access_token = refresh.access_token
        return Response({'refresh': str(refresh),'access': str(access_token),}, status=status.HTTP_200_OK)

class TokenRefresh(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"message": "Refresh token is required.", "status":False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = refresh.access_token
            return Response({'access': str(new_access_token)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Invalid refresh token.", "status":False}, status=status.HTTP_400_BAD_REQUEST)

def has_permission(user, required_permissions):
    if not user.is_authenticated:
        return (False, "Unauthorized User")

    user_permissions = UserAuth.objects.filter(user__id=user.pk, permissions__name__in=required_permissions).values_list("permissions__name", flat=True)
    missing_permissions = set(required_permissions) - set(user_permissions)
    if missing_permissions: return (False, f"Permission denied: Missing required permissions.")
    return (True, "Permission granted")



