from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'id')
    list_display_links = ('email', 'username')
    ordering = ['-date_joined']
    readonly_fields = ('date_joined', 'updated_at')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'username')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('updated_at', 'date_joined')}),
    )

admin.site.register(User, CustomUserAdmin)
