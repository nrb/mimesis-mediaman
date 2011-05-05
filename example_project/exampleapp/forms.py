from django.forms import ModelForm, CharField
from mediaman.utils import add_media_selector
from exampleapp.models import Something


class SomethingForm(ModelForm):
    class Meta:
        model = Something


SomethingForm = add_media_selector(SomethingForm)
