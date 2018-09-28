import csv
import os
from io import StringIO
import json

from functools import wraps
from dateutil.parser import parse

from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import DeleteView, CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404

from mainapp.models import Author, Book, Tag, URL_ITEMS, URL_DICT
from mainapp.forms import FORM_DICT, AutorSearchForm, BookSearchForm, TagSearchForm


def add_slash(val):
    return '/' + val + '/'


def main(request):
    context = {'url_list': URL_ITEMS}
    context['page_name'] = 'Выберите одну из таблиц'
    return render(request, 'mainapp/index.html', context)


class BaseView(ListView):

    def get_context_data(self, *args, **kwargs):
        self.page = self.request.GET.get('page', None)
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)

        try:
            result_query = paginator.page(self.page)
        except PageNotAnInteger:
            result_query = paginator.page(1)
        except EmptyPage:
            result_query = paginator.page(paginator.num_pages)

        context['model'] = self.model._meta.verbose_name_plural
        context['url_pref'] = add_slash(self.model.Other.url)
        context['result_query'] = result_query
        return context


class BaseViewObj(SingleObjectMixin):

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk', -1)
        model_str = self.kwargs.get('model_str', None)
        if model_str in URL_DICT.keys():
            obj = get_object_or_404(URL_DICT[model_str], pk=pk)
        else:
            obj = None
        return obj


class BooksList(BaseView, ListView):

    model = Book
    template_name = 'mainapp/lists.html'
    paginate_by = 10

    def get_queryset(self):
        request = self.request
        if request.method == 'POST':
            self.allow_empty = True
        if request.is_ajax():
            if request.method == 'GET':
                author = request.GET.get('id_author', '')
                tag = request.GET.get('id_tag', '')
                pub_date = request.GET.get('id_publication_date', '')
                search = request.GET.get('id_search', '')
                query_list = []
                if search:
                    search__regex = r'^.*{}.*$'.format(search.lower())
                    query_list.append(
                        Q(
                            fname__regex=search__regex) | Q(
                            mname__regex=search__regex) | Q(
                            lname__regex=search__regex) | Q(
                            namel__regex=search__regex) | Q(
                            descl__regex=search__regex))

                if author:
                    query_list.append(Q(author__pk=author))
                if tag:
                    query_list.append(Q(tags__pk__in=[tag, ]))
                if pub_date:
                    try:
                        pub_date = parse(pub_date)
                    except ValueError:
                        pass
                    except OverflowError:
                        pass
                    else:
                        query_list.append(Q(publication_date=pub_date))
                try:
                    self.template_name = 'mainapp/includes/inc__lists.html'
                    result = Book.objects.annotate(
                        fname=Lower('author__first_name'),
                        mname=Lower('author__middle_name'),
                        lname=Lower('author__last_name'),
                        namel=Lower('name'),
                        descl=Lower('description')).filter(
                        *query_list)
                    return result
                except ValidationError:
                    self.allow_empty = True
            else:
                self.allow_empty = True
        else:
            return super().get_queryset()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ignore_col'] = ['id', 'description', 'tags', ]
        context['col_names'] = self.model.get_field_names_gen(
            context['ignore_col'])
        context['page_name'] = 'Список книг'
        context['search'] = BookSearchForm()
        return context


class TagsList(BaseView, ListView):

    model = Tag
    template_name = 'mainapp/lists.html'
    paginate_by = 10

    def get_queryset(self):
        request = self.request
        if request.method == 'POST':
            self.allow_empty = True
        if request.is_ajax():
            if request.method == 'GET':
                name = request.GET.get('id_search', '')
                is_active = request.GET.get('id_is_active', '')
                query_list = []
                if name:
                    search__regex = r'^.*{}.*$'.format(name.lower())
                    query_list.append(Q(name_l__regex=search__regex))
                if is_active:
                    if is_active == '1':
                        is_active = [True, ]
                    elif is_active == '0':
                        is_active = [False, ]
                    else:
                        is_active = [True, False, ]
                    query_list.append(Q(is_active__in=is_active))
                try:
                    self.template_name = 'mainapp/includes/inc__lists.html'
                    return Tag.objects.annotate(
                        name_l=Lower('name')).filter(
                        *query_list)
                except ValidationError:
                    self.allow_empty = True
            else:
                self.allow_empty = True
        else:
            return super().get_queryset()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ignore_col'] = []
        context['col_names'] = self.model.get_field_names_gen()
        context['page_name'] = 'Список тегов'
        context['search'] = TagSearchForm()
        return context


class AuthorsList(BaseView, ListView):

    model = Author
    template_name = 'mainapp/lists.html'
    paginate_by = 10

    def get_queryset(self):
        request = self.request
        if request.method == 'POST':
            self.allow_empty = True
        if request.is_ajax():
            if request.method == 'GET':
                search = request.GET.get('id_search', '')
                if search:
                    search = search.lower()
                    search__regex = r'.*{}.*'.format(search)
                    query_list = [
                        Q(
                        fname__regex=search__regex) | Q(
                        mname__regex=search__regex) | Q(
                        lname__regex=search__regex) | Q(
                        emaill__regex=search__regex), 
                        ]
                else:
                    query_list = []
                try:
                    self.template_name = 'mainapp/includes/inc__lists.html'
                    annotate = Author.objects.annotate(
                        fname=Lower('first_name'),
                        mname=Lower('middle_name'),
                        lname=Lower('last_name'),
                        emaill=Lower('email'))
                    result = annotate.filter(*query_list)
                    return result
                except ValidationError:
                    self.allow_empty = True
            else:
                self.allow_empty = True
        else:
            return super().get_queryset()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ignore_col'] = []
        context['col_names'] = self.model.get_field_names_gen()
        context['page_name'] = 'Перечень авторов'
        context['search'] = AutorSearchForm()
        return context

    #def dispatch(self, request, *args, **kwargs):
    #    if request.is_ajax() and request.GET.get('model', None) is not None:
    #        try:
    #            model = request.GET.get('model', None)
    #            ref = request.GET.get('ref', None)
    #            pk = request.GET.get('pk', -1)
    #            model = URL_DICT[model]
    #            filter_dict = {ref + '__pk': pk}
    #            result = model.objects.filter(**filter_dict).values()
    #            result = ({"data": list(result)})
    #        except BaseException:
    #            result = json.dumps({"data": []})
    #        finally:
    #            return JsonResponse(result)
    #    else:
    #        return super().dispatch(request, *args, **kwargs)


class Add(CreateView):

    model = None
    form_class = None
    success_url = ''
    template_name = 'mainapp/add.html'

    def get_form_class(self):
        self.model_str = self.kwargs.get('model_str', None)
        if self.model_str in URL_DICT.keys():
            self.model = URL_DICT[self.model_str]
            self.success_url = reverse_lazy(f'mainapp:{self.model_str}_list')
            return FORM_DICT[self.model_str]

    def get_context_data(self, *args, **kwargs):
        self.context = super().get_context_data(*args, **kwargs)
        self.context['model_name'] = self.model._meta.verbose_name
        return self.context


class Edit(BaseViewObj, UpdateView):

    model = None
    template_name = 'mainapp/edit.html'
    success_url = ''

    def get_object(self, queryset=None):
        return super(Edit, self).get_object(queryset=None)

    def get_form_class(self):
        self.model_str = self.kwargs.get('model_str', None)
        if self.model_str in URL_DICT.keys():
            self.model = URL_DICT[self.model_str]
            self.success_url = reverse_lazy(f'mainapp:{self.model_str}_list')
            return FORM_DICT[self.model_str]

    def get_context_data(self, *args, **kwargs):
        self.context = super().get_context_data(*args, **kwargs)
        self.context['model_name'] = self.model._meta.verbose_name
        return self.context


class Details(BaseViewObj, DetailView):

    model = ''
    template_name = 'mainapp/details.html'

    def get_object(self, queryset=None):
        return super().get_object(queryset=None)

    def get_context_data(self, *args, **kwargs):
        self.context = super().get_context_data(*args, **kwargs)
        #self.context['referer'] = self.request.META.get('HTTP_REFERER', '/')

        model_str = self.kwargs.get('model_str', None)
        if model_str in URL_DICT.keys():
            model = URL_DICT[model_str]
            self.context['col_names'] = model.get_field_names_gen()
            self.context['col_m2m'] = model.get_m2m_field_names_gen()
            self.context['model_name'] = model._meta.verbose_name
            self.context['url_pref'] = add_slash(model.Other.url)
        return self.context


class Delete(BaseViewObj, DeleteView):

    model = ''
    success_url = '/'

    def get_object(self, queryset=None):
        return super().get_object(queryset=None)


def get_other(request, *args, **kwargs):
    a = 1
    return HttpResponse('ok')
