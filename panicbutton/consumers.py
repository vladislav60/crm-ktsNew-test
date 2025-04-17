import json
from channels.generic.websocket import AsyncWebsocketConsumer
from panicbutton.redis_connection import RedisConnectionManager

redis_manager = RedisConnectionManager()

class AlarmConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]

        if not user.is_authenticated:
            await self.close()
            return

        self.user_id = str(user.id)
        self.channel_name_key = f"user:{self.user_id}"

        # Сохраняем новое соединение в Redis и завершаем старое, если оно есть
        await redis_manager.set_user_channel(user.id, self.channel_name)

        self.group_name = "alarms"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print(f"✅ Подключён: user_id={self.user_id}, channel={self.channel_name}")

    async def disconnect(self, close_code):
        user = self.scope["user"]
        if user.is_authenticated:
            # Удаляем channel_name из Redis
            await redis_manager.delete_user_channel(user.id)

            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            print(f"🔌 Отключён: user_id={user.id}, channel={self.channel_name}")

    async def send_alarm(self, event):
        await self.send(text_data=json.dumps(event["message"]))