from django.db import models
from django.conf import settings

class Group(models.Model):
    name = models.CharField("群组名称", max_length=100)
    description = models.TextField("群组描述", blank=True, null=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_groups',
        verbose_name="创建者"
    )
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "群组"
        verbose_name_plural = verbose_name


class GroupMember(models.Model):
    ROLE_CHOICES = (
        ('管理员', '管理员'),
        ('普通成员', '普通成员')
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name="所属群组"
    )
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='group_memberships',
        verbose_name="成员"
    )
    role = models.CharField("角色", max_length=10, choices=ROLE_CHOICES, default='普通成员')
    joined_at = models.DateTimeField("加入时间", auto_now_add=True)

    class Meta:
        unique_together = ('group', 'member')
        verbose_name = "群成员"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.member


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name="发送者"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages',
        verbose_name="接收者",
        blank=True,
        null=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='mymessages',
        verbose_name="所属群组",
        blank=True,
        null=True
    )
    content = models.TextField("消息内容")
    created_at = models.DateTimeField("发送时间", auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "消息"
        verbose_name_plural = verbose_name