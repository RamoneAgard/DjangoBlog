from django.db import models
from django.conf import settings
# Create your models here.
User = settings.AUTH_USER_MODEL

# class BlogCommentManager(models.Manager):
#     def getComments(self, user, title, timestamp):
#         return self.get_queryset().filter(user=user, title=title, timestamp=timestamp)

class BlogComment(models.Model):
    user = models.ForeignKey(User, null = True, on_delete=models.SET_NULL)
    blog_post = models.ForeignKey('blog.BlogPost', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
