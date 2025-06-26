from django.db import models
from django.contrib.auth.models import AbstractUser

# 性别选择项
GENDER_CHOICES = [
    ('M', '男'),
    ('F', '女'),
    ('U', '未知'),
]
# 隐私账户选择项
PROFILE_VISIBILITY_CHOICES = [
    ('public', '公开账户'),
    ('friend', '好友账户'),
    ('privacy', '私密账户'),
]

class User(AbstractUser):
    username = models.CharField(verbose_name='用户名',max_length=20,unique=True)
    nickname = models.CharField(verbose_name='昵称', max_length=50,default='匿名用户',blank=True,null=True)
    telephone = models.CharField(verbose_name='手机号',max_length=11,null=True,blank=True)
    bio = models.TextField(verbose_name="个人简介",blank=True, null=True)
    avatar = models.ImageField(verbose_name="头像",upload_to='avatars/', blank=True, null=True)
    gender = models.CharField(verbose_name="性别",max_length=1, choices=GENDER_CHOICES, default='U')
    profile_visibility = models.CharField(verbose_name="账户可见性",max_length=10, choices=PROFILE_VISIBILITY_CHOICES, default='public')
    birthday = models.DateField(verbose_name="生日",blank=True, null=True)
    register_at = models.DateTimeField(verbose_name="注册时间",auto_now_add=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
