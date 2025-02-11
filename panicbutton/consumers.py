import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AlarmConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f"🚀 Подключение WebSocket от {self.scope['user']}")
        # Проверяем, авторизован ли пользователь
        if self.scope["user"].is_authenticated:
            self.group_name = "alarms"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            print(f"✅ Пользователь {self.scope['user']} добавлен в группу 'alarms'")
        else:
            print("❌ Неавторизованный пользователь пытается подключиться")
            await self.close()

    async def disconnect(self, close_code):
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            print(f"🔴 Пользователь {self.scope['user']} покинул группу 'alarms'")

    async def send_alarm(self, event):
        await self.send(text_data=json.dumps(event["message"]))