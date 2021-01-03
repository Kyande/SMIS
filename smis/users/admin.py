from django.contrib import admin

from .models import User


def reactivate_users(modeladmin, request, queryset):
    queryset.update(is_active=True)


reactivate_users.short_description = "Activate selected users"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    actions = [reactivate_users]
    date_hierarchy = 'date_joined'
    empty_value_display = '-empty-'
    exclude = ('date_joined', 'is_active', )
    fields = (
        'avatar',
        ('first_name', 'last_name'),
        'email',
        'user_type',
        'is_superuser',
        'is_staff',
    )
    list_display = (
        'email', 'first_name', 'last_name',
        'date_joined', 'user_type', 'is_active',
        'is_staff')
    list_display_links = ('email', )
    list_filter = ('user_type', 'is_active', 'is_staff', )
    list_per_page = 50
    ordering = ('first_name', 'last_name', )
    search_fields = ('first_name', 'last_name', 'email')
