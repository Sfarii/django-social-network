from django.urls import path, re_path

from . import views
from . import consumers


urlpatterns = (
    path('new/room', views.CreateRoomView.as_view(), name='create_room'),
    path('rooms/', views.RoomListView.as_view(), name='list_rooms', kwargs={'slug': None}),
    path('room/<str:slug>/chat', views.RoomDetailView.as_view(), name='detail_room'),

    path('room/<str:slug>/delete', views.DeleteRoomView.as_view(), name='delete_room'),
    path('create/room/for/<str:username>', views.CreateRoomForUserView.as_view(), name='create_room_for_user')
)