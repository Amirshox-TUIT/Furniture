from django.db import models


class BlogManager(models.Manager):
    def get_queryset(self):
        return super(BlogManager, self).get_queryset().filter(status="published")
