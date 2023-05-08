from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import Blog, CustomUser


class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at','image',)
    list_filter = ('author', 'created_at',)
    search_fields = ('title', 'text')
    date_hierarchy = 'created_at'


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'username', 'is_staff','role',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups',)
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
    fieldsets = (
        (None, {'fields': ('email', 'password','role',)}),
        (_('Personal Info'), {'fields': ('username',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined',)}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('username','email', 'password1', 'password2','role',)}),
    )


admin.site.register(Blog, BlogAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

