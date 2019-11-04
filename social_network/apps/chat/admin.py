from django.contrib import admin
from django.db.models.constants import LOOKUP_SEP

from .models import Room, Message


class MessageInline(admin.StackedInline):
    model = Message
    classes = ('collapse', )
    extra = 0
    readonly_fields = ('sender', )
    list_select_related = ('sender__profile', )

    def get_queryset(self, request):
        return super(MessageInline, self).get_queryset(request).select_related(*self.list_select_related).order_by('-created')

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(MessageInline, self).get_formset(request, obj, **kwargs)
        formset.sender = request.user
        return formset


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    view_on_site = False
    fields = ('name', 'avatar', 'participants')
    inlines = (MessageInline, )
    list_display = ('name', 'get_participants')

    def get_participants(self, obj):
        return ", ".join([participant.get_full_name() for participant in obj.participants.all()])