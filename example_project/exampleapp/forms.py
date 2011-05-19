from django.forms import ModelForm, CharField
from mediaman.forms import MediaModelForm
from exampleapp.models import Something


class SomethingForm(MediaModelForm):
    class Meta:
        model = Something
