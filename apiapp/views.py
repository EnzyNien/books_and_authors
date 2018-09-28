import csv
import os
from io import StringIO

from django.shortcuts import get_object_or_404, Http404
from rest_framework import generics
from apiapp.serializers import AuthorSerializer, BookSerializer, TagSerializer, SRLZR_DICT
from mainapp.models import URL_DICT


class BaseApi():

    def get_serializer_class(self):
        params = self.request.parser_context.get('kwargs', None)
        if isinstance(params, dict):
            try:
                model_str = params['model_str']
                self.model = URL_DICT[model_str]
                return SRLZR_DICT[model_str]
            except KeyError:
                pass
        raise Http404()


class ApiAdd(BaseApi, generics.CreateAPIView):
    serializer_class = None

    def get_serializer_class(self):
        return super().get_serializer_class()


class ApiEdit(BaseApi, generics.RetrieveUpdateAPIView):

    def get_serializer_class(self):
        return super().get_serializer_class()

    def get_queryset(self):
        pk = self.kwargs.get('pk', '')
        model = self.kwargs.get('model_str', '')
        model_obj = URL_DICT[model]
        try:
            return model_obj.objects.filter(pk=pk)
        except KeyError:
            pass
        raise Http404()


class ApiList(BaseApi, generics.ListAPIView):

    serializer_class = None
    queryset = None

    def get_queryset(self):
        params = self.request.parser_context.get('kwargs', None)
        if isinstance(params, dict):
            try:
                model_str = params['model_str']
                model_obj = URL_DICT[model_str]
                return model_obj.objects.all()
            except KeyError:
                pass
        raise Http404()


class ApiDetails(BaseApi, generics.RetrieveAPIView):

    serializer_class = None
    queryset = None

    def get_queryset(self):
        pk = self.kwargs.get('pk', '')
        model = self.kwargs.get('model_str', '')
        model_obj = URL_DICT[model]
        try:
            return model_obj.objects.filter(pk=pk)
        except KeyError:
            pass
        raise Http404()

    def get_serializer_class(self):
        return super().get_serializer_class()


class ApiDelete(BaseApi, generics.DestroyAPIView):

    serializer_class = None
    queryset = None

    def get_object(self):
        pk = self.kwargs.get('pk', '')
        model = self.kwargs.get('model_str', '')
        model_obj = URL_DICT[model]
        try:
            return get_object_or_404(model_obj, pk=pk)
        except KeyError:
            pass
        raise Http404()

    def get_serializer_class(self):
        return super().get_serializer_class()
