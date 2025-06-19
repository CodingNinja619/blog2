from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
import os
import uuid
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import post_init
from faker import Faker
from taggit.managers import TaggableManager
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField 
from django.contrib.auth import get_user_model
class User(AbstractUser):
    pass

def get_file_path(instance, filename):
    ext = filename.rsplit(".", 1)[1]
    allowed_extensions = ["jpg", "jpeg", "png", "gif", "svg", "webp"]
    if ext not in allowed_extensions:
        raise ValidationError("This file's extension isn't allowed")
    filename = f"{uuid.uuid4()}.{ext}"

    return os.path.join("post_images/", filename)

class Post(models.Model):
    title = models.CharField(max_length=255)
    # body = models.TextField()
    body = RichTextUploadingField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=1000, null=True, blank=True)
    tags = TaggableManager(blank=True)
    read_later_users = models.ManyToManyField(get_user_model(), related_name='read_later_posts')

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.id])

def slugifyOnModelCreation(**kwargs):
    instance = kwargs.get("instance")
    instance.slug = slugify(instance.title)

post_init.connect(slugifyOnModelCreation, Post)

class Image(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=get_file_path)
    post = models.ForeignKey(Post, 
                             on_delete=models.CASCADE, 
                             default=1, related_name='images')  # foreign key is because
                                                                                                # later I might want to store multiple images
                                                                                                # per post
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



class PostFactory:
    fake = Faker()

    @staticmethod
    def create(title=None, body=None, author=None):
        title = title or PostFactory.fake.sentence()
        body = body or PostFactory.fake.paragraph()
        author = author or User.objects.first()
        slug = slugify(title)
        return Post.objects.create(title=title, body=body, author=author, slug=slug)
         
    
    @staticmethod
    def create_batch(amount, title=None, body=None, author=None):
        for _ in range(amount):
            PostFactory.create(title, body, author)

