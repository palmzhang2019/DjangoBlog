from django.utils.safestring import mark_safe
from django.conf.urls import url
from stark.service.stark import site, ModelStark
from .models import *
from django.shortcuts import HttpResponse, redirect


site.register(UserInfo)
site.register(Blog)
site.register(Category)
site.register(Tag)

class KeywordsConfig(ModelStark):
    list_display = ["word", "article"]

site.register(Keywords, KeywordsConfig)
site.register(Article)
site.register(Article2Tag)
site.register(ArticleDetail)
