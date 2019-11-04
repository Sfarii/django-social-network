from django import forms

from .models import Room, Message


class RoomForm(forms.ModelForm):
    def __init__(self, current_user, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        self.current_user = current_user
        self.fields['participants'].queryset = self.fields['participants'].queryset.exclude(pk=self.current_user.pk)

    class Meta:
        model = Room
        fields = ('name', 'avatar', 'participants')

    def save(self, commit=True):
        instance = super(RoomForm, self).save()
        instance.participants.add(self.current_user)
        if commit:
            instance.save()
        return instance


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('body', )