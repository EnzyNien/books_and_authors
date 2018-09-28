from collections import Iterable

from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.conf import settings

class BaseUtil():
    
    @classmethod
    def get_field_names_gen(cls, stop_list=None):
        return_list = []
        if not isinstance(stop_list,Iterable):
            stop_list = ['id',]
        fields = [f
            for f in cls._meta.get_fields()
            if f.concrete and (
                not f.is_relation
                or f.one_to_one
                or (f.many_to_one and f.related_model)
            )
        ]
        for item in fields:
            if item.name in stop_list:
                continue
            upload_to = None
            if isinstance(item,models.ImageField):
                upload_to = item.upload_to
            return_list.append([item.name,upload_to,])
        return return_list

    @classmethod
    def get_m2m_field_names_gen(cls):
        return_list = []
        fields = [
            (f, f.model if f.model != cls else None)
            for f in cls._meta.get_fields()
            if f.many_to_many and not f.auto_created
        ]
        for item in fields:
            return_list.append(item[0].name)
        return return_list

class Author(models.Model, BaseUtil):
    #1. Автор
    #1.1. Фамилия (обязательное поле)
    #1.2. Имя (обязательное поле)
    #1.3. Отчество (необязательное поле)
    #1.4. Электронная почта (необязательное поле)
    #1.5. Телефон (необязательное поле) 

    phone_regex = RegexValidator(regex=r'^\+?1?\d{12}$', message="Телефонный номер должен иметь формат: '+99999999999'. До 12 цифр.")

    first_name = models.CharField(
        verbose_name = 'Имя',
        max_length=100, 
        blank=False,
        null=False)

    last_name = models.CharField(
        verbose_name = 'Фамилия',
        max_length=100, 
        blank=False,
        null=False)

    middle_name = models.CharField(
        verbose_name = 'Отчество',
        max_length=100, 
        blank=True,
        null=True)

    email = models.EmailField(
        verbose_name = 'Электронная почта',
        blank=True,
        null=True)

    phone = models.CharField(
        verbose_name = 'Телефон', 
        validators=[phone_regex], 
        max_length=15, 
        blank=True,
        null=True)
    
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        
    class Other:
        url = 'authors'

    def __str__(self):
        last_name_ = self.last_name if self.last_name else ''
        first_name_ = self.first_name if self.first_name else ''
        middle_name_ = self.middle_name if self.middle_name else ''
        return f"{last_name_} {first_name_} {middle_name_}"

class Tag(models.Model, BaseUtil):
    #2. Тег
    #2.1. Название (обязательное поле)
    #2.2. Флаг активности 

    name = models.CharField(
        verbose_name = 'Название', 
        max_length = 150, 
        blank = False,
        null = False)

    is_active = models.BooleanField(
        verbose_name = 'Флаг активности',
        default = False, 
        blank = False)

    class Meta:
        verbose_name = 'Teг'
        verbose_name_plural = 'Теги'
       
    class Other:
        url = 'tags'

    def __str__(self):
        return f"{self.name}"

class Book(models.Model, BaseUtil):
    #3. Книга
    #3.1. Название (обязательное поле)
    #3.2. Дата публикации (обязательное поле)
    #3.3. Краткое описание (обязательное поле)
    #3.4. Изображение-превью (необязательное поле)
    #3.5. Автор (внешний ключ, обязательное поле)
    #3.6. Теги (m2m, необязательное поле) 

    name = models.CharField(
        verbose_name = 'Название', 
        max_length=250, 
        blank=False,
        null=False)

    publication_date = models.DateField(
        verbose_name = 'Дата публицации',
        default = timezone.now, 
        blank=True,
        null=True)

    description = models.TextField(
        verbose_name = 'Краткое описание', 
        blank=True,
        null=True)

    image = models.ImageField(
        verbose_name = 'Изображение-превью', 
        upload_to=settings.BOOK_IMAGE,
        blank=True,
        null=True)

    author = models.ForeignKey(
        Author, 
        verbose_name = 'Автор',
        on_delete=models.CASCADE)

    tags = models.ManyToManyField(
        Tag, 
        verbose_name = 'Теги',
        blank=True)

    class Meta:
        ordering = ['author__id', 'name']
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    class Other:
        url = 'books'
    
    def __str__(self):
        return f"{self.name} {str(self.publication_date)}"

MODEL_LIST= [Author,Book,Tag]
URL_ITEMS = [[item.Other.url, item._meta.verbose_name_plural] for item in MODEL_LIST]
URL_DICT = {item.Other.url:item for item in MODEL_LIST}