import re

from django.forms import ModelForm, CharField, Textarea, ValidationError

from mimesis.models import MediaUpload
from taggit.forms import TagWidget
from taggit.utils import parse_tags


class TagField(CharField):
    
    widget = TagWidget
    
    def clean(self, value):
        try:
            # only accept letters, digits, and spaces
            if re.search(r'[^a-zA-Z0-9 ]', value) is not None:
                raise ValueError
            return parse_tags(value.lower())
        except ValueError:
            raise ValidationError(_('Please provide a space-separated list of tags.'))


class MetadataForm(ModelForm):
    
    caption = CharField(widget=Textarea, max_length=500)
    tags = TagField(help_text='Separate tags with spaces.')
    
    class Meta:
        model = MediaUpload
        fields = ('caption', 'tags')
