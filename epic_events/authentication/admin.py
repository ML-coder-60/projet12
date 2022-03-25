from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    """
        A form for :
            creating new users.
                Includes required fields:
                  'username',
                  'team',
                  'is_active',
                  'password',
                  'password2'
            list/set users
                Includes fields:
                  'username',
                  'team',
                  'status'
            Filter users by:
                  'username',
                  'team',
                  'status'
    """
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'team', 'is_active')
    list_filter = ('team', 'is_active')

    search_fields = ("username",)
    ordering = ("username",)
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Status', {'fields': ('is_active',)}),
        ('Permissions', {'fields': ('team',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'team', 'is_active', 'password', 'password2'),
        }),
    )


admin.site.register(User, UserAdmin)

# Disable group on Interface
admin.site.unregister(Group)
