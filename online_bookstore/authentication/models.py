from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name=None, password=None, is_staff=False, is_superuser=False, is_admin=False):
        if not email:
            raise ValueError("The Email field is required.")
        if not username:
            raise ValueError("The Username field is required.")
        if not first_name:
            raise ValueError("The First Name field is required.")
        if not password:
            raise ValueError("The Password field is required.")
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_admin=is_admin,
            is_active=True
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name=None, password=None):
        user = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True,
            is_superuser=True,
            is_admin=True
        )
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    updated_at = models.DateTimeField(auto_now=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.username} ({self.email})"

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

class Permission(models.Model):
    name = models.CharField(max_length=100)
    admin = models.BooleanField(default=False)
    user = models.BooleanField(default=False)
    super_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    updated_at = models.DateTimeField(auto_now=timezone.now)

    def __str__(self):
        return self.name
    
class UserAuth(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission, blank=True)
    otp = models.CharField(max_length=20,blank=True,null=True)
    otp_validated_upto = models.DateTimeField(blank=True,null=True)
    verified = models.BooleanField(default=False)
    login = models.BooleanField(default=False)
    logout = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    updated_at = models.DateTimeField(auto_now=timezone.now)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
