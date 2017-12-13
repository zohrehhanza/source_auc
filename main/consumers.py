import json
from channels import Channel
from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user
from .settings import MSG_TYPE_LEAVE, MSG_TYPE_ENTER, NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS
from .models import Room
from .utils import get_room_or_error, catch_client_error
from .exceptions import ClientError



@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    message.channel_session['rooms'] = []
    print("ws_connect!!!!!!")
    Group('users').send({
        'text': json.dumps({
        'mymessage': 'This new user logged in !!!!' ,
        })
    })
   


def ws_receive(message):

    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel("chat.receive").send(payload)
    print("ws_Recieve!!!!!!")

@channel_session_user
def ws_disconnect(message):
    for room_id in message.channel_session.get("rooms", set()):
        try:
            room = Room.objects.get(pk=room_id)
            print("ws_discnnect!!!!!!")
            room.websocket_group.discard(message.reply_channel)
        except Room.DoesNotExist:
            pass


@channel_session_user
#@catch_client_error
def chat_join(message):

    room = get_room_or_error(message["room"], message.user)

    if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        print(message.user)
        print(MSG_TYPE_ENTER)
        room.send_message(None, message.user, MSG_TYPE_ENTER)

    room.websocket_group.add(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).union([room.id]))
    print("ws_join!!!!!!")
    message.reply_channel.send({
        "text": json.dumps({
            "join": str(room.id),
            "title": room.title,
        }),
    })

@channel_session_user
#@catch_client_error
def chat_leave(message):
    room = get_room_or_error(message["room"], message.user)

    if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        room.send_message(None, message.user, MSG_TYPE_LEAVE)
    print("ws_leave!!!!!!")
    room.websocket_group.discard(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).difference([room.id]))
    message.reply_channel.send({
         "text": json.dumps({
            "leave": str(room.id),
        }),
    })

@channel_session_user
#@catch_client_error
def chat_send(message):
    if int(message['room']) not in message.channel_session['rooms']:
        raise ClientError("ROOM_ACCESS_DENIED")
    room = get_room_or_error(message["room"], message.user)
    print("ws_chat_send!!!!!!")
    room.send_message(message["message"], message.user)


