from django.contrib import admin

from core.models import *


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('text', 'time', 'author')
    list_filter = ('time',)
    search_fields = ['author__username', 'text']


@admin.register(User_Pic)
class User_PicAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'avatar'
                    )


@admin.register(MessageFile)
class MessageFileAdmin(admin.ModelAdmin):
    list_display = ('file',)