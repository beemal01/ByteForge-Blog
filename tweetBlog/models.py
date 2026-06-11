from django.db import models
from authAccount.models import MyUser
from django.conf import settings
from django.utils.text import slugify

class content(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blogs"
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    blog_body = models.TextField(max_length=10500)
    featured_image = models.ImageField(upload_to='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title