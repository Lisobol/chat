from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser




class Message(models.Model):
    text = models.TextField(verbose_name='Текст сообщения',blank=False)
    time = models.DateTimeField(verbose_name='Дата',auto_now_add=True)
    author = models.ForeignKey(User,verbose_name='Автор',on_delete=models.CASCADE)
    # picture = models.ImageField(upload_to='static/core/files/',null=True, blank=True)
    # chat = models.ForeignKey(Chat,on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.text


class User_Pic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='media/',null=True,blank=True)

    def __str__(self):
        return self.user.username

class MessageFile(models.Model):
    file = models.ImageField(upload_to='media/messages/',null=True,blank=True)

