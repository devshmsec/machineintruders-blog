from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=40)
    slug = models.SlugField(max_length=50)
    author = models.ForeignKey(
        User, default="alphaomega", on_delete=models.CASCADE)
    description = models.TextField(max_length=200)
    thumbnail = models.ImageField(
        upload_to="thumbnails/", default="thumbnails/default.jpg")
    tags = TaggableManager(blank=True)
    content = RichTextUploadingField()
    like = models.ManyToManyField(User, related_name='like', blank=True)
    posted_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title} by {self.author}.'

    def get_absolute_url(self):
        url = reverse("detail", args=[str(self.id), str(self.slug)])
        return url


@receiver(pre_save, sender=Post)
def slugger(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey(
        'self', null=True, on_delete=models.CASCADE, related_name='replies')
    text = models.TextField(max_length=200)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} - {}'.format(self.text, str(self.user.username))


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default='profile/default.png',
                              upload_to='profile/')

    def __str__(self):
        return f"{self.user.username}'s profile"


def create_profile(sender, **kwargs):
    if kwargs['created']:
        profile = Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
