from channels.generic.websocket import AsyncWebsocketConsumer
import json


# This file is alternative for views.py for asgi 


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # modern way => self.room_group_name = f"chat{self.room_name}"
        self.room_group_name = 'chat%s' % self.room_name 

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    """  TEST MESSAGE FOR LEARNING

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'test_message',
                'tester':'hello world !',
                'user':'admin',
            }
        )

    
    async def test_message(self, event):
        tester = event['tester']
        user = event['user']
        print(event)

        # converting dict object to json string to pass to front end.
        await self.send(text_data=json.dumps({
            'tester_c':tester,
            'user':user,
        }))
    """

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.room_name,
        )

    # recieve message from frontend to websocket function
    async def receive(self, text_data):
        # converting json string to dict '{'message':message}' string  => {'message':message} dictionary
        text_data_obj = json.loads(text_data) 
        message = text_data_obj['message']
        username = text_data_obj['username']
        print(text_data_obj)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chatroom_message',
                'message':message,
                'username':username,
            }
        )
    

    # send message to frontend function
    async def chatroom_message(self, event):
        message = event.get('message')
        user = event.get('username')

        # to make dict_object to json string
        await self.send(text_data=json.dumps({
            'message':message,
            'username':user,
        }))
