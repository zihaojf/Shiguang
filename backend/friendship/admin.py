from django.contrib import admin
from .models import Friendship

@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ['id','user_a','user_b','status','remark','created_at','updated_at']
    list_filter = list_display

    