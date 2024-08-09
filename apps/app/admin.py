from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = ('title', 'date')
    list_filter = ('date',)

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)