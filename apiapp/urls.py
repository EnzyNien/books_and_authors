from django.conf.urls import url, include
from apiapp import views

app_name = 'apiapp'


urlpatterns = [
	url('^(?P<model_str>\w+)/add/', views.ApiAdd.as_view(), name='api_add'),
    url('^(?P<model_str>\w+)/(?P<pk>\d+)/delete/', views.ApiDelete.as_view(), name='api_delete'),
    url('^(?P<model_str>\w+)/(?P<pk>\d+)/edit/', views.ApiEdit.as_view(), name='api_edit'),
    url('^(?P<model_str>\w+)/(?P<pk>\d+)/details/', views.ApiDetails.as_view(), name='api_details'),
    url('^(?P<model_str>\w+)/list/', views.ApiList.as_view(), name='api_list'),
]

