from rest_framework import serializers
from .models import User, UserAuth, Permission
from .helpers import email_validator

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'is_admin']

    def to_internal_value(self, data):
        if not(type(data)==dict and len(data.keys())==5 and all(key in data for key in ["email", "first_name", "last_name", "is_admin", "password"])):
            raise serializers.ValidationError({"message": "Invalid request data."})

        email, password, first_name = data.get("email"), data.get("password"), data.get("first_name")
        last_name, is_admin = data.get("last_name"), data.get("is_admin")
        if not all((field and type(field)==str) for field in [email, password, first_name]):
            raise serializers.ValidationError({"message": "Invalid or missing request data."})
        if (last_name and type(last_name) not in (str, type(None))) or type(is_admin)!=bool :
            raise serializers.ValidationError({"message": "Invalid or missing request data."})
        if not email_validator(email=email):
            raise serializers.ValidationError({"message": "Invalid email."})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"message": "User with this email already exists."})

        return super().to_internal_value(data)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data.get('last_name', None),
            password=validated_data['password'],
            is_admin=validated_data['is_admin']
        )

        user_auth_obj = UserAuth.objects.create(user=user)
        if user.is_admin:
            permission_objects = Permission.objects.filter(admin=True)
        else:
            permission_objects = Permission.objects.filter(user=True)
        user_auth_obj.permissions.set(permission_objects)

        return user

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'is_admin', 'is_active']

    def to_internal_value(self, data):
        if not(type(data)==dict and len(data.keys())==6 and all(key in data for key in ["user_id", "email", "first_name", "last_name", "is_admin", "is_active"])):
            raise serializers.ValidationError({"message": "Invalid request data."})
        
        email, user_id, first_name = data.get("email"), data.get("user_id"), data.get("first_name")
        last_name, is_admin, is_active = data.get("last_name"), data.get("is_admin"), data.get("is_active")
        if not(email and type(email)==str and first_name and type(first_name)==str):
            raise serializers.ValidationError({"message": "Invalid or missing request data."})
        if (last_name and (type(last_name) not in (str, type(None)))) or type(is_admin)!=bool or type(is_active)!=bool or type(user_id)!=int :
            raise serializers.ValidationError({"message": "Invalid or missing request data."})
        if not email_validator(email=email):
            raise serializers.ValidationError({"message": "Invalid email."})
        
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise serializers.ValidationError({"message": "User with this email already exists."})

        return super().to_internal_value(data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email')
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.is_admin = validated_data.get('is_admin')
        instance.is_active = validated_data.get('is_active')
        
        instance.save()

        user_auth_obj = UserAuth.objects.filter(user=instance).first()
        if user_auth_obj:
            user_auth_obj.permissions.clear()
            if instance.is_admin:
                permission_objects = Permission.objects.filter(admin=True)
            else:
                permission_objects = Permission.objects.filter(user=True)

            user_auth_obj.permissions.set(permission_objects)

        return instance

