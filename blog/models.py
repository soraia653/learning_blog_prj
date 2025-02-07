from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


class User(AbstractUser):
    user_image = models.ImageField(
        default='defaults/default-image.png',
        upload_to='user_images/'
    )


class Post(models.Model):
    PUBLICATION_STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=125, unique=True)
    slug_title = models.SlugField(max_length=255, unique=True)
    summary = models.TextField(max_length=200)
    image_url = models.URLField(
        blank=True,
        default='https://fdczvxmwwjwpwbeeqcth.supabase.co/storage/v1/object/public/images/25c93125-bd78-407b-930d-a430f0f23ec4/b4c86719-0619-4bd2-b3f1-b14a25982b43.png'
    )
    body = RichTextField(null=True, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=9,
        choices=PUBLICATION_STATUS_CHOICES,
        default='published'
    )

    tags = TaggableManager()

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug_title = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):

    username = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_date']

    def __str__(self) -> str:
        return f"Comment by {self.username} to post {self.post}"
