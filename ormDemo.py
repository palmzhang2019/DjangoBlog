import os

from django.db.models import Count

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DaidaiStudy.settings")

    import django
    django.setup()

    from app01 import models

    user = models.UserInfo.objects.filter(username="admin").first()

    ret = models.Article.objects.filter(user=user).extra(
        select = {
            "archive_ym": "date_format(create_time, '%%Y-%%m')"
        }
    ).values("archive_ym").annotate(c=Count("nid")).values("archive_ym", "c")
    print(ret)