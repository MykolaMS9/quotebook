from django.conf import settings
from django.forms import ModelForm, CharField, TextInput, Textarea, DateField
from .models import Tag, Quote, Author


class TagForm(ModelForm):
    name = CharField(max_length=25, required=True, widget=TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Tag
        fields = ['name']


class QuoteForm(ModelForm):
    quote = CharField(min_length=5, max_length=300, required=True, widget=Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = Quote
        fields = ['quote']
        exclude = ['author', 'tags']


class AuthorForm(ModelForm):
    fullname = CharField(required=True, widget=TextInput(attrs={"class": "form-control"}))
    born_date = DateField(required=True, input_formats=settings.DATE_INPUT_FORMATS, widget=TextInput(attrs={"class": "form-control"}))
    born_location = CharField(required=True, widget=TextInput(attrs={"class": "form-control"}))
    description = CharField(max_length=250, required=True, widget=Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']
