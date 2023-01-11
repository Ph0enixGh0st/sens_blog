from django.contrib import admin
from blog.models import Post, Tag, Comment
from django.contrib.auth.models import User


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_at')
    raw_id_fields = ('author',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'published_at')
    raw_id_fields = ('post',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
