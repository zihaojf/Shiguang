from django.db import models
from django.conf import settings

# 动态权限选择项
POST_VISIBILITY_CHOICES = [
    ('public', '公开可见'),
    ('friend', '好友可见'),
]

class Post(models.Model):
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,verbose_name="发布者",)
    title = models.CharField(max_length=200,verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    visibility = models.CharField(max_length=20, choices=POST_VISIBILITY_CHOICES, default='public',verbose_name="可见性")
    likes = models.IntegerField(default=0,verbose_name="点赞数")
    comments = models.IntegerField(default=0,verbose_name="评论数")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="发布时间")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="更新时间")

    class Meta:
        verbose_name = "动态帖子"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,verbose_name="所属动态")
    liker = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name="点赞用户")
    create_at = models.DateTimeField(auto_now_add=True,verbose_name="点赞时间")

    class Meta:
        verbose_name = "动态点赞"
        verbose_name_plural = verbose_name
        unique_together = (('post','liker'),)
