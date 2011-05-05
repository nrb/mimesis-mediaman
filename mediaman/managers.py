from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.utils.datastructures import SortedDict

#from mimesis.models import MediaUpload
from django.db.models.loading import get_model

class MediaAssociationManager(models.Manager):
    
    def for_model(self, model, content_type=None):
        """
        QuerySet returning all media for a particular model (either an
        instance or a class).
        """
        ct = content_type or ContentType.objects.get_for_model(model)
        qs = self.get_query_set().filter(content_type=ct)
        if isinstance(model, models.Model):
            qs = qs.filter(object_pk=force_unicode(model._get_pk_val())).select_related('media')
        return qs

    def attach_to(self, obj_list, content_type=None):
        """
        Attaches all relevant mimesis media to objects within a list or 
        queryset.  Assumes all items in the list or queryset are of the same
        type (checks only the first item).
        """
        
        if len(obj_list) < 1:
            return None
            
        ct = content_type or ContentType.objects.get_for_model(obj_list[0])
        
        object_dict = SortedDict()
        for item in obj_list:
            object_dict[item.id] = item
                
        associations = self.get_query_set().filter(
            object_pk__in=object_dict.keys(), content_type=ct
        ).select_related('media')
        
        for asso in associations:
            if asso.is_primary == True:
                object_dict[asso.object_pk].pri_img_url = asso.media.media.url
                object_dict[asso.object_pk].pri_caption = asso.media.caption
                object_dict[asso.object_pk].pri_media = asso.media
            try:
                object_dict[asso.object_pk].media.append(asso.media)
            except AttributeError:
                object_dict[asso.object_pk].media = [asso.media]
        
        return object_dict.values()
