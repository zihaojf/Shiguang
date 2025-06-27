from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','post','user','parent_comment','content','likes','created_at']
    list_filter = ['post','parent_comment','user']
    search_fields = list_display