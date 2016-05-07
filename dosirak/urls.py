# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from dosirak import views

urlpatterns=patterns('',url(r'^$',views.index,name='index'),
                     #/dosirak/

                     #  /dosirak/5/
url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),#namve value as called by the {%url%}template code
    # ex: /dosirak/5/results/
url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
url(r'^(?P<question_id>\d+)/again/$', views.again, name='again'),
    # ex: /polls/5/vote/
url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
)
