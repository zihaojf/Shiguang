from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'nickname', 'telephone', 'bio', 'gender','birthday','profile_visibility','register_at')
    search_fields = list_display
    list_filter = list_display


