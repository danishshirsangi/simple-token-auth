from django.contrib import admin
from django.contrib.auth.models import Group
from .models import UserCustom, DonorDonee
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.


class UserAdmin(admin.ModelAdmin):
     fieldsets = (
        ('User credentials', {
            'fields': ('email', 'password', 'is_active', 'is_admin')
        }),
        ('User Required', {
            'fields': ('blood_group', 'gender', 'age')
        }),
        ('User Info', {
            'fields': ('first_name', 'last_name','mobile','address'),
        }),
    )


admin.site.register(UserCustom, UserAdmin)
admin.site.register(DonorDonee)


admin.site.unregister(Group)
