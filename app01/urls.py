from django.conf.urls import url
from app01 import views


urlpatterns = [
    url(r'(\w+)/article/(\d+)/$', views.article_detail),
    url(r'search/', views.search),
    url(r'category/(\w+)/$', views.category),
    url(r'tag/(\w+)/$', views.tag),
    url(r'archive/(\d{4}-\d{2})/$', views.archive),
    url(r'backend/add_article/', views.add_article),
    url(r'up_down/$', views.up_down),
    url(r'comment/$', views.comment),
    url(r'comment_tree/(\d+)/$', views.comment_tree),
    url(r'(\w+)/$', views.home),
]