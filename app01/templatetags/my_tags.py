from django import template
from django.db.models import Count
from app01 import models


register = template.Library()

@register.inclusion_tag('left_menu.html')
def get_left_menu(username):
    if not username:
        category_list = models.Category.objects.all().annotate(c=Count("article")).values("title", "c")
        tag_list = models.Tag.objects.all().annotate(c=Count("article")).values("title", "c")
        archive_list = models.Article.objects.all().extra(
            select={
                "archive_ym": "date_format(create_time,'%%Y-%%m')"
            }
        ).values("archive_ym").annotate(c=Count("nid")).values("archive_ym", "c")
        return {
            "category_list": category_list,
            "tag_list": tag_list,
            "archive_list": archive_list
        }
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog
    category_list = models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
    tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
    archive_list = models.Article.objects.filter(user=user).extra(
        select={
            "archive_ym":"date_format(create_time,'%%Y-%%m')"
        }
    ).values("archive_ym").annotate(c=Count("nid")).values("archive_ym","c")

    return {
        "category_list": category_list,
        "tag_list": tag_list,
        "archive_list": archive_list
    }