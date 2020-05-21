from django import template
from app01 import models


register = template.Library()

@register.inclusion_tag('mainImage.html')
def showMainImage(article_id):
    mainImage = models.Article.objects.filter(pk=article_id).values("mainPicture")
    if mainImage[0].get("mainPicture"):
        return {
            "mainImage": mainImage[0].get("mainPicture")
        }
    else:
        return {
            "mainImage": "/addArticleImage/default.jpg"
        }
