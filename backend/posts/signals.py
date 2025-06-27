from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Like,Post

@receiver(post_save,sender=Like)
def update_likes_on_like(sender,instance,created,**kwargs):
    if created:
        instance.post.likes += 1
        instance.post.save()

@receiver(post_delete,sender=Like)
def update_likes_on_unlike(sender,instance,**kwargs):
    instance.post.likes -= 1
    instance.post.save()


