import re

from django.forms import CharField, HiddenInput
from django.forms.util import ErrorList
from django.contrib.contenttypes.models import ContentType

from taggit.models import Tag
from mimesis.models import MediaAssociation, MediaUpload


def _attach_for_form(form):
    def attach_mimesis_media(instance=None):
        if not instance:
            instance = form.instance
        to_attach = form.cleaned_data['mimesis_attached_media'].split(',')
        if to_attach[0]:
            primary_id = int(to_attach[0])
            to_attach = set([int(id) for id in to_attach])
        else:
            primary_id = None
            to_attach = set()
        current = set(MediaAssociation.objects.for_model(instance).values_list('media_id', flat=True))
        to_del = MediaAssociation.objects.filter(
            content_type=ContentType.objects.get_for_model(instance),
            object_pk=instance.pk,
            media__in=(current - to_attach)
        ).delete()
        MediaAssociation.objects.for_model(instance).filter(is_primary=True).update(is_primary=False)
        for media in MediaUpload.objects.filter(id__in=(to_attach - current)):
            MediaAssociation.objects.create(
                media=media,
                content_object=instance,
                is_primary=(media.id == primary_id)
            )
        if primary_id in current:
            MediaAssociation.objects.for_model(instance).filter(media__id=primary_id).update(is_primary=True)
    return attach_mimesis_media


def add_media_selector(FormClass):
    def constructor(*args, **kwargs):
        form = FormClass(*args, **kwargs)
        initial_media = ''
        instance = kwargs.get('instance')
        if instance:
            initial_media = ','.join([str(pk) for pk in MediaAssociation.objects.for_model(instance).values_list('media_id', flat=True)])
        form.fields['mimesis_attached_media'] = CharField(required=False, widget=HiddenInput(), initial=initial_media)
        form.attach_mimesis_media = _attach_for_form(form)
        return form
    constructor.__name__ = FormClass.__name__
    return constructor


def tags_from_string(phrase):
    ignore_list = ['a', 'an', 'as', 'at', 'before', 'but', 'by', 'for', 'from',
        'is', 'in', 'into', 'like', 'of', 'off', 'on', 'onto', 'per', 'since',
        'than', 'the', 'this', 'that', 'to', 'up', 'via', 'with']
    word_list = re.findall(r'[A-Za-z0-9]+', phrase.lower())
    word_list = [word for word in word_list if word not in ignore_list]
    return Tag.objects.filter(name__in=word_list).values_list('name', flat=True)
