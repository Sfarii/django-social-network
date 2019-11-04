from django.contrib import admin

from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'phone', 'address', 'birthday', 'language')

    def get_user(self, obj):
        return obj.user.get_full_name()