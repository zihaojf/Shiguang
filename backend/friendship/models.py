from django.db import models
from django.conf import settings

class Friendship(models.Model):
    user_a = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,verbose_name='本用户',related_name='sent_friendship')
    user_b = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,verbose_name='好友',related_name='received_friendship')
    STATUS_CHOICES = [
        ('已接受','已接受'),('待确认','待确认'),('已拒绝','已拒绝')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='待确认',verbose_name='好友关系状态')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="发送时间")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="更新时间")
    remark = models.CharField(max_length=60,blank=True,null=True,verbose_name='好友备注')


