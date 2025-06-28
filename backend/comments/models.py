from django.db import models
from posts.models import Post
from django.conf import settings


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,verbose_name="所属帖子",related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,verbose_name="评论者")
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,related_name='children',verbose_name='父评论 ')
    content = models.TextField(verbose_name='评论内容')
    likes = models.IntegerField(default=0,verbose_name='评论点赞数')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='评论更新时间 ')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
