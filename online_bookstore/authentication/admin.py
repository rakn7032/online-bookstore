from django.contrib import admin
from . import models
 
class UserAdmin(admin.ModelAdmin):
    list_display=("id","email","username","first_name", "is_active", "is_staff", "is_superuser", "is_admin")
    fields = ("email","username","first_name","last_name", "is_active", "is_staff", "is_superuser", "is_admin", "date_joined","created_at","updated_at")
    readonly_fields=("created_at","updated_at")

class PermissionAdmin(admin.ModelAdmin):
    list_display=("id", "name", "super_admin", "admin", "user")
    fields = ("name", "super_admin", "admin", "user" ,"created_at","updated_at")
    readonly_fields=("created_at","updated_at")

class UserAuthAdmin(admin.ModelAdmin):
    list_display=("id", "user", "otp", "otp_validated_upto", "verified", "login", "logout")
    fields = ("user", "permissions", "otp", "otp_validated_upto", "verified", "login", "logout" ,"created_at", "updated_at")
    readonly_fields=("created_at","updated_at")
    
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Permission, PermissionAdmin)
admin.site.register(models.UserAuth, UserAuthAdmin)
