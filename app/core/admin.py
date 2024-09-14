"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'username', 'phone_number']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'phone_number')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',
                                           'created_at',
                                           'updated_at')}),
    )
    readonly_fields = ['last_login', 'created_at', 'updated_at']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'username',
                'phone_number',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


admin.site.register(models.User, UserAdmin)
