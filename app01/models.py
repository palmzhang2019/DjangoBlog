from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserInfo(AbstractUser):
    nid = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.FileField(upload_to="avatars/", default="avatars/default.png", verbose_name="avatar")
    create_time = models.DateField(auto_now_add=True)

    blog = models.OneToOneField(to="Blog", to_field="nid", null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = verbose_name + 's'

class Blog(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    site = models.CharField(max_length=32, unique=True)
    theme = models.CharField(max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "BlogSite"
        verbose_name_plural = verbose_name + "s"

class Category(models.Model):
    nid = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=32)
    blog = models.ForeignKey(to="Blog", to_field="nid")
    nike_name = models.CharField(max_length=32, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = verbose_name + "s"

class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, unique=True)
    blog = models.ForeignKey(to="Blog", to_field="nid")
    nike_name = models.CharField(max_length=32, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = verbose_name + "s"

class Keywords(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article", to_field="nid", null=True)
    word = models.CharField(max_length=16)

    def __str__(self):
        return self.word

class Article(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name="ArticleTitle")
    mainPicture = models.FileField(upload_to="articleMainPic/", null=True, verbose_name="mainPicture")
    desc = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)

    # comment count
    comment_count = models.IntegerField(verbose_name="CommentCount", default=0)
    # thumbs up
    thumbs_up_count = models.IntegerField(verbose_name="ThumbsUpCount", default=0)
    unlike_count = models.IntegerField(verbose_name="UnlikeCount", default=0)

    category = models.ForeignKey(to="Category", to_field="nid", null=True)
    user = models.ForeignKey(to="UserInfo", to_field="nid")
    tags = models.ManyToManyField(
        to="Tag",
        through="Article2Tag",
        through_fields=("article", "tag")
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = verbose_name + "s"

class Article2Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article", to_field="nid")
    tag = models.ForeignKey(to="Tag", to_field="nid")

    def __str__(self):
        return "{}-{}".format(self.article.title, self.tag.title)

    class Meta:
        unique_together = (("article", "tag"))
        verbose_name = "Article-Tag"
        verbose_name_plural = verbose_name + "s"

class ArticleDetail(models.Model):
    nid = models.AutoField(primary_key=True)
    content = models.TextField()
    article = models.OneToOneField(to="Article", to_field="nid")

    def __str__(self):
        return "{}".format(self.article.title)

    class Meta:
        verbose_name = "ArticleDetail"
        verbose_name_plural = verbose_name +"s"

class ArticleUpDown(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="UserInfo", null=True)
    article = models.ForeignKey(to="Article", null=True)
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = (("article", "user"))
        verbose_name = "ArticleThumbsUp"
        verbose_name_plural = verbose_name + "s"

class Comment(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article", to_field="nid")
    user = models.ForeignKey(to="UserInfo", to_field="nid")
    content = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey("self", null=True, blank=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = verbose_name + "s"