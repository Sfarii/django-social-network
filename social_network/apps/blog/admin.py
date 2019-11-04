from django.contrib import admin

from . import models


class CommentInline(admin.StackedInline):
    model = models.Comment
    extra = 0
    readonly_fields = ('author', )
    list_select_related = ('author', )

    def get_queryset(self, request):
        return super(CommentInline, self).get_queryset(request).select_related(*self.list_select_related).order_by('-created')

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(CommentInline, self).get_formset(request, obj, **kwargs)
        formset.sender = request.user
        return formset


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'cover', 'body', 'status', 'author')
    inlines = (CommentInline, )
    list_display = ('title', 'get_author', 'status', 'published', 'created', 'updated')

    def get_queryset(self, request):
        queryset = super(PostAdmin, self).get_queryset(request)
        queryset = queryset.select_related('author').prefetch_related('author__profile', 'comments', 'comments__author')
        return queryset

    def get_author(self, obj):
        return obj.author.get_full_name()

    get_author.short_description = 'Author'
