from tokenize import Comment

from django.contrib import admin
from .models import Post,Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id","title","publisher","content","visibility","likes","comments","created_at","updated_at"]
    list_filter = ["id","title","publisher","content","visibility","likes","comments"]

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ["post","liker","create_at"]
    list_filter = ["post","liker"]
    