from django.contrib import admin

from post.models import Tag, Post, Comment


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("author")
        return queryset


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("author")
        return queryset
