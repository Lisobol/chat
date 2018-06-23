from django.contrib import admin
from core.models import *
from django.contrib.auth.models import User


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('text', 'time', 'author')
    list_filter = ('time',)
    search_fields = ['author__username', 'text']



# @admin.register(User)
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     empty_value_display = 'null'
#     list_display = ('username', 'password')
#     list_filter = ('username',)
#     search_fields = ['username', 'password']

