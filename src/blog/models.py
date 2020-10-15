from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from django.utils.text import slugify
from .utils import random_string_generator

# Create your models here.
User = settings.AUTH_USER_MODEL

class BlogPostQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(publish_date__lte=now)

    def search(self, query):
        lookup = (  Q(title__icontains=query) |
                    Q(content__icontains=query) |
                    Q(slug__icontains=query) |
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query) |
                    Q(user__username__icontains=query)
                    )
        return self.filter(lookup)

class BlogPostManager(models.Manager):
    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)

class BlogPost(models.Model): #user.blogpost_set.all()  or BlogPost.objects.filter(user = user instance)--> get querySet associated with a user
    # id = models.IntegerField() or 'pk' (primary key) --- this is added implicitly
    user = models.ForeignKey(User, default=1, null = True, on_delete=models.SET_NULL)
    # deleting a user sets there posts to default user if set or null if set true.
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    title = models.CharField(max_length=120, unique=False)
    slug = models.SlugField(unique=True)
    content = models.TextField(null=True, blank=True)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    #
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    objects = BlogPostManager()

    # unique slug generator retrieved from online resource, user does not need to create their own slug
    def unique_slug_generator(self, new_slug=None):
        """
        This is for a Django project and it assumes your instance
        has a model with a slug field and a title character (char) field.
        """
        if new_slug is not None:
            slug = new_slug
        else:
            slug = slugify(self.title)

        Klass = self.__class__
        qs_exists = Klass.objects.filter(slug=slug).exists()
        if qs_exists:
            new_slug = "{slug}-{randstr}".format(
                        slug=slug,
                        randstr=random_string_generator(size=4)
                    )
            return self.unique_slug_generator(new_slug=new_slug)
        return slug

    # overridden save to create an auto generated slug for the new post
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.unique_slug_generator()
        super().save(*args, **kwargs)


    class Meta:
        ordering = ['-publish_date', '-updated', 'timestamp']

    def get_absolute_url(self):
        return f"/blog/{self.slug}"

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit/"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete/"
