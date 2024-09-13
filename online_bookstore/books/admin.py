from django.contrib import admin
from . import models
 
class BookAdmin(admin.ModelAdmin):
    list_display=("id", "title","author", "published_date", "price")
    fields = ("title","author","description", "published_date", "price", "created_at", "updated_at")
    readonly_fields=("created_at","updated_at")
 
admin.site.register(models.Book, BookAdmin)

