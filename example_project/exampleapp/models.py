from django.db import models

from taggit.managers import TaggableManager


class Something(models.Model):
    name = models.CharField(max_length=100)
    tags = TaggableManager()
    
    def __unicode__(self):
        return self.name
