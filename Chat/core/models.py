from datetime import timezone

from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    text = models.TextField(verbose_name='Текст сообщения')
    time = models.DateTimeField(verbose_name='Дата',auto_now_add=True)
    author = models.ForeignKey(User,verbose_name='Автор',on_delete=models.CASCADE)

    chat = models.ForeignKey(Chat,on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.text


class ChatUser(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return str(self.id)

#
# class ChatMessage(models.Model):
#     message = models.ForeignKey(Message, on_delete=models.CASCADE)
#     chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
#     id = models.AutoField(primary_key=True)
#
#     def __str__(self):/
#         return str(self.id)


class Chat(models.Model):
    id = models.AutoField(primary_key=True)


    def __str__(self):
        return str(self.id)
