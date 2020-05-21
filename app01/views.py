import io
import json, os, re
from bs4 import BeautifulSoup
from django.db.models import Count, F
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib import auth
from geetest import GeetestLib
from app01 import forms, models
from DaidaiStudy import settings
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from app01.utils.page import Pagination


# Create your views here.

pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"

def login(request):
    if request.method =="POST":
        ret = {"status": 0, "msg": ""}
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]

        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            user = auth.authenticate(username = username, password = pwd)
            if user:
                auth.login(request, user)
                ret["msg"] = "/index/"
            else:
                ret["status"] = 1
                ret["msg"] = "Incorrect username or password"
        else:
            ret['status'] = 1
            ret['msg'] = 'Incorrect Captcha'

        return JsonResponse(ret)
    return render(request, "login.html")

# logout
def logout(request):
    auth.logout(request)
    return redirect("/index/")

def get_valid_img(request):
    from PIL import Image, ImageDraw, ImageFont
    import random

    def get_random_color():
        return random.randint(0,255), random.randint(0, 255), random.randint(0,255)

    # create a image
    image_obj = Image.new(
        "RGB",
        (220, 35),
        get_random_color()
    )

    # write some words
    # create a Draw object
    draw_obj = ImageDraw.Draw(image_obj)
    # load Font
    font_obj = ImageFont.truetype("static/font/kumo.tff", 28)
    tmp_list = []
    for i in range(5):
        u = chr(random.randint(65, 90))
        l = chr(random.randint(97, 122))
        n = chr(random.randint(0,9))

        tmp = random.choice([u,l,n])
        tmp_list.append(tmp)
        draw_obj.text((20+40*i, 0), tmp, fill=get_random_color(), font = font_obj)

    request.session["valid_code"] = "".join(tmp_list)

    from io import BytesIO
    io_obj = BytesIO()

    image_obj.save(io_obj, "png")
    data = io_obj.getvalue()
    return HttpResponse(data)

# handle geetest
def get_geetest(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    request_str = gt.get_response_str()
    return HttpResponse(request_str)

def register(request):
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        form_obj = forms.RegForm(request.POST)
        if form_obj.is_valid():
            form_obj.cleaned_data.pop("re_password")
            avatar_image = request.FILES.get("avatar")
            img = Image.open(avatar_image)
            if img.width > 200:
                img.thumbnail((200, 200))
            imgByteArr = io.BytesIO()
            img.save(imgByteArr, format="JPEG")
            img = InMemoryUploadedFile(
                imgByteArr,
                field_name= avatar_image.field_name,
                name = avatar_image.name,
                content_type = avatar_image.content_type,
                size = 1000,
                charset=None
            )
            models.UserInfo.objects.create_user(**form_obj.cleaned_data, avatar = img)
            ret["msg"] = "/index/"
            return JsonResponse(ret)
            # return HttpResponse("ok")
        else:
            ret['status'] = 1
            ret['msg'] = form_obj.errors
            return JsonResponse(ret)

    # generate a form object
    form_obj = forms.RegForm()
    # print(form_obj.fields)
    return render(request, "register.html", {"form_obj": form_obj})

def check_username_exist(request):
    ret = {"status": 0, "msg": ""}
    username = request.GET.get("username")
    is_exist = models.UserInfo.objects.filter(username=username)
    if is_exist:
        ret["status"] = 1
        ret["msg"] = "Username has been registered"
    return JsonResponse(ret)

def article_detail(request, username, pk):
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("404")
    blog = user.blog
    # find this article
    article = models.Article.objects.filter(pk=pk).first()
    search_keywords = models.Article.objects.filter(pk=pk).values("keywords__word")
    key = ""
    for search_keyword in search_keywords:
        key += '{},'.format(search_keyword.get('keywords__word'))
    key = key.rstrip(',')
    # all comments
    comment_list = models.Comment.objects.filter(article_id=pk)
    tkd = {
        "title": article.title,
        "keywords": key,
        "description": article.desc
    }
    return render(
        request,
        "article_detail.html",
        locals()
    )

def get_left_menu(username):
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog
    category_list = models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
    tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")

    archive_list = models.Article.objects.filter(user=user).extra(
        select={
            "archive_ym":"date_format(create_time,'%%Y-%%m')"
        }
    ).values("archive_ym").annotate(c=Count("nid")).values("archive_ym","c")

    return category_list, tag_list, archive_list

def up_down(request):
    article_id = request.POST.get('article_id')
    is_up = json.loads(request.POST.get("is_up"))
    user = request.user
    response = {"state": True}
    try:
        models.ArticleUpDown.objects.create(user=user, article_id = article_id, is_up = is_up)
        if is_up:
            models.Article.objects.filter(pk=article_id).update(thumbs_up_count=F("thumbs_up_count")+1)
        else:
            models.Article.objects.filter(pk=article_id).update(unlike_count=F("unlike_count")+1)
    except:
        response["state"] = False
        response['is_updb'] = models.ArticleUpDown.objects.filter(user=user, article_id = article_id).first().is_up

    return JsonResponse(response)

def comment(request):
    if request.method == "POST":
        pid = request.POST.get("parent_comment")
        article_id = request.POST.get("article")
        user_id = request.POST.get("user")
        content = request.POST.get("content")
        response = {}
        if not pid:
            comment_obj = models.Comment.objects.create(article_id=article_id, user_id = user_id, content = content)
        else:
            comment_obj = models.Comment.objects.create(article_id=article_id, user_id = user_id, content = content, parent_comment_id=pid )
        response["create_time"] = comment_obj.create_time# .strftime("%Y-%m-%d %H:%i:%s")
        response['content'] = comment_obj.content
        return JsonResponse(response)
    else:
        return HttpResponse("Not Ok")

def comment_tree(request, article_id):
    ret = list(models.Comment.objects.filter(article_id = article_id).values("pk", "content", "parent_comment_id", "create_time"))

    return JsonResponse(ret, safe=False)

def checkxss(content):
    content = re.sub(r"&lt;script&gt;.*?&lt;/script&gt;", "", content)
    return content

def add_article(request):
    category_list = models.Category.objects.all()
    tag_list = models.Tag.objects.all()
    if request.method =="POST":
        title = request.POST.get('title')
        article_content = request.POST.get('article_content')
        keywords = request.POST.get("keywords", "")
        category_id = request.POST.get("category", "")
        tags = request.POST.getlist("tags", "")

        user = request.user
        bs = BeautifulSoup(article_content, "html.parser")
        for tag in bs.find_all():
            if tag.name in ["script", "link"]:
                tag.decompose()
        desc = str(bs.text)[:150]
        mainImage = request.FILES.get("mainImage")
        if not mainImage:
            ret = re.search(r'src="/media/(\w+/.*?.\w{3,4})"', article_content)
            if ret:
                mainImage = ret.groups()[0]
        # 生成article新增对象
        article = models.Article.objects.create(
            title=title,
            user = user,
            desc=desc,
            mainPicture = mainImage,
            category_id=category_id,
        )
        if keywords:
            keywords = keywords.split(',')
            queryset = []
            for key in keywords:
                queryset.append(models.Keywords(word=key, article=article))
            models.Keywords.objects.bulk_create(queryset)
        if tags:
            queryset = []
            for tag in tags:
                queryset.append(models.Article2Tag(tag_id=tag, article_id=article.pk))
            # tag表
            models.Article2Tag.objects.bulk_create(queryset)
        models.ArticleDetail.objects.create(content=(str(bs)), article = article)
        return redirect("/index/")
    return render(request, "add_article.html", locals())

def upload(request):
    obj = request.FILES.get("upload_img")
    img = Image.open(obj)
    if img.width> 700:
        img.thumbnail((700, 700))

    img_path = os.path.join(settings.MEDIA_ROOT, 'addArticleImage/'+obj.name)
    img.save(img_path)
    # with open(img_path, "wb") as f:
    #     for line in obj:
    #         f.write(line)
    res = {
        "error":0,
        "url": "/media/addArticleImage/"+obj.name
    }
    return JsonResponse(res)

def uploadMainImage(request):
    obj = request.FILES.get("mainImage")
    img = Image.open(obj)
    if img.width> 700:
        img.thumbnail((700, 700))

    img_path = os.path.join(settings.MEDIA_ROOT, 'addArticleImage/'+obj.name)
    img.save(img_path)

    res = {
        "error":0,
        "url": "/media/mainImage/"+obj.name
    }
    return JsonResponse(res)

def get_page(request, article_list):
    current_page = int(request.GET.get("page",1))
    data_count = article_list.count()
    base_path = request.path

    pagination = Pagination(current_page, data_count, base_path, request.GET, per_page_num=10, pager_count=9)
    article_list = article_list[pagination.start:pagination.end]
    return pagination, article_list

def index(request):
    article_list = models.Article.objects.all().order_by("-create_time")
    # for article in article_list:
    #     print(article.tags.all())
    tkd = {
        "title": "呆呆爱学习",
        "keywords": "Python学习,日语学习,学习笔记",
        "description": "张小呆的学习笔记"
    }
    pagination, article_list = get_page(request, article_list)
    return render(request, "index.html", locals())

def home(request, username):
    user = models.UserInfo.objects.filter(username= username).first()
    if not user:
        return HttpResponse("404")
    blog = user.blog
    article_list = models.Article.objects.filter(user=user).order_by("-create_time")
    pagination, article_list = get_page(request, article_list)
    return render(
        request,
        "home.html",
        locals()
    )

def category(request, cat_name):
    article_list = models.Article.objects.filter(category__title=cat_name).order_by("-create_time")
    pagination, article_list = get_page(request, article_list)
    tkd = {
        "title": cat_name
    }
    return render(
        request,
        "category.html",
        locals()
    )

def tag(request, tag_name):
    tagObj = models.Tag.objects.filter(title = tag_name).first()
    article_list = tagObj.article_set.all().order_by("-create_time")
    pagination, article_list = get_page(request, article_list)
    tkd = {
        "title": tag_name
    }
    return render(
        request,
        "category.html",
        locals()
    )

def archive(request, ym):
    year = ym.split('-')[0]
    month = ym.split('-')[1]
    article_list = models.Article.objects.filter(create_time__istartswith=ym)
    pagination, article_list = get_page(request, article_list)
    tkd = {
        "title": "{}年{}月".format(year,month)
    }
    return render(request, "archive.html", locals())

def search(request):
    keyword = request.GET.get("q", "")
    tkd = {
        "title": "{}的搜索结果".format(keyword)
    }
    if keyword:
        article_list = models.Article.objects.filter(title__contains=keyword)
        return render(request, "index.html", locals())
    else:
        return redirect("/index/")