from django.db import models
import os
import random
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.urls import reverse
from django.contrib.auth.models import User




def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_name = random.randint(1, 324345344332)
    name, ext = get_filename_ext(filename)
    # final_name = f"{new_name}{ext}"
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"products/{final_name}"


# Create your models here.


# CRUD --> database
# Create => POST
# Read or Retrieve --> list or single or search => GET
# Update => PUT or PATCH or POST
# Delete => DELETE

class ProductQuerySet(models.query.QuerySet):
    def get_featured(self):
        return self.filter(featured=True)

    def active(self):
        return self.filter(active=True)


class ProductManager(models.Manager):

    def all(self):
        return self.get_queryset().active()

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def get_featured(self):
        return self.get_queryset().filter(featured=True)

    def get_featured_active(self):
        return self.get_queryset().filter(featured=True)

    def get_by_id(self, productId):
        qs = self.get_queryset().filter(id=productId)  # product.objects
        if qs.count() == 1:
            return qs.first()
        return None


class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2, default=10.36)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(
        User, related_name='like', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')

    def get_absolute_url(self):
        # return f"/products/{self.slug}"
        return reverse("products:detail", kwargs={"slug": self.slug})

    objects = ProductManager()

    def __str__(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)
