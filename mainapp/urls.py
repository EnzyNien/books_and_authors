from django.conf.urls import url, include
from mainapp import views

app_name = 'mainapp'


urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^books/$', views.BooksList.as_view(), name='books_list'),
    url(r'^tags/$', views.TagsList.as_view(), name='tags_list'),
    url(r'^authors/$', views.AuthorsList.as_view(), name='authors_list'),
    url(r'^authors/(?P<data>\w+)/(?P<pk>\d+)/$', views.get_other, name='authors_list'),
	url('^add/(?P<model_str>\w+)/', views.Add.as_view(), name='add'),
    url('^delete/(?P<model_str>\w+)/(?P<pk>\d+)/', views.Delete.as_view(), name='delete'),
    url('^edit/(?P<model_str>\w+)/(?P<pk>\d+)/', views.Edit.as_view(), name='edit'),
    url('^details/(?P<model_str>\w+)/(?P<pk>\d+)/', views.Details.as_view(), name='details'),
]

