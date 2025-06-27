from django.contrib import admin
from .models import Group,GroupMember,Message

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id','name','description','creator','created_at']
    search_fields = list_display

@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ['id','group','member','role','joined_at']
    search_fields = list_display

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id','sender','receiver','content','created_at']
    search_fields = list_display


