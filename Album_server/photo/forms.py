from django import forms

from .models import Photo
from .models import Images
from .models import Key


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('title', 'content', )

class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ('image', 'photoId', )

class KeyForm(forms.ModelForm):
    class Meta:
        model = Key
        fields = ('name', 'key', )
