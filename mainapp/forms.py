
import django.forms as forms
from django.forms.widgets import DateInput

from mainapp.models import URL_DICT, Author, Book, Tag

def add_form_control_class(fields):
    for _, field in fields.items():
        field.widget.attrs['class'] = "form-control"

def add_additional_class(fields):
    for _, field in fields.items():
        field.widget.attrs['class'] += " query-class"

class AuthorAddEditForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AuthorAddEditForm, self).__init__(*args, **kwargs)
        add_form_control_class(self.fields)

class TagAddEditForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TagAddEditForm, self).__init__(*args, **kwargs)
        add_form_control_class(self.fields)

class BookAddEditForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BookAddEditForm, self).__init__(*args, **kwargs)
        add_form_control_class(self.fields)
        self.fields['tags'].queryset = Tag.objects.filter(is_active = True)
        self.fields['publication_date'].widget=forms.TextInput(attrs={'type': 'date', 'class' : 'form-control'})

class AutorSearchForm(forms.Form):
    search = forms.CharField(max_length=150,
        label = 'Поиск по частям имени авторов и email',
        required=False)

    def __init__(self, *args, **kwargs):
        super(AutorSearchForm, self).__init__(*args, **kwargs)
        add_form_control_class(self.fields)
        add_additional_class(self.fields)

class BookSearchForm(forms.Form):

    search = forms.CharField(max_length=150,
        label = 'Поиск по подстроке в названии книги, описании, имени автора',
        required=False)
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(), 
        empty_label='-------',
        label = 'Поиск по автору из списка',
        required=False)
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.filter(is_active=True),
        empty_label='-------',
        label = 'Поиск по тегу из списка',
        required=False)
    publication_date = forms.DateField(
        label = 'Поиск по дате публикации', 
        widget=forms.TextInput(attrs={'type': 'date'}),
        required=False)

    def __init__(self, *args, **kwargs):
        super(BookSearchForm, self).__init__(*args, **kwargs)
        add_form_control_class(self.fields)
        add_additional_class(self.fields)

class TagSearchForm(forms.Form):

    search = forms.CharField(
        max_length=Tag._meta.get_field('name').max_length,
        label = 'Поиск по наименванию',
        required=False)
    is_active = forms.BooleanField(
        label = 'Отбор по активности',
        required=False)

    def __init__(self, *args, **kwargs):
        super(TagSearchForm, self).__init__(*args, **kwargs)
        add_form_control_class(self.fields)
        add_additional_class(self.fields)

FORM_DICT = {Author.Other.url:AuthorAddEditForm,
            Book.Other.url:BookAddEditForm,
            Tag.Other.url:TagAddEditForm,
            }