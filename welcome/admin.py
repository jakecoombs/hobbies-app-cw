from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import PageView, User

# Register your models here.


class PageViewAdmin(admin.ModelAdmin):
    list_display = ['hostname', 'timestamp']

admin.site.register(PageView, PageViewAdmin)
admin.site.register(User, UserAdmin)
