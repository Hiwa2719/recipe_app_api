from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Tag


@admin.register(User)
class UserModelAdmin(BaseUserAdmin):
    ordering = None
    list_display = '__str__', 'is_staff', 'is_active'
    list_filter = 'is_active', 'is_staff', 'is_superuser', 'date_joined'
    date_hierarchy = 'date_joined'
    search_fields = 'email', 'name',
    readonly_fields = 'date_joined',
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    filter_horizontal = 'user_permissions', 'groups'


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    pass
