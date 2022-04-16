from django.contrib import admin

from core.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'created_at', 'is_published')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'created_at')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Post, PostAdmin)
