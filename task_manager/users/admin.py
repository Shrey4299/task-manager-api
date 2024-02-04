from django.contrib import admin
from .models import RegisterUser
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea
from django import forms
from django.db import models


class UserAdminConfig(UserAdmin):
    model = RegisterUser
    search_fields = ('email', 'name', 'phone_number')
    list_filter = ('is_active', 'is_staff',)
    ordering = ('-start_date',)
    list_display = ('email', 'name', 'phone_number', 'is_active', 'is_staff', 'premium')  # Add 'premium' field here
    fieldsets = (
        (None, {'fields': ('email', 'name', 'phone_number', 'premium',)}),  # Add 'premium' field here
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Important dates', {'fields': ('start_date',)}),
        ('Custom Fields', {'fields': ('spam',)}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone_number', 'premium', 'password1', 'password2', 'is_active', 'is_staff')}  # Add 'premium' field here
         ),
    )


admin.site.register(RegisterUser, UserAdminConfig)

