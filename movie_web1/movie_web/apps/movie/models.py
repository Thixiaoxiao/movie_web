from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


# Create your models here.


class Nation(models.Model):
    name = models.CharField(max_length=20, verbose_name="国家", unique=True)
    is_showon_subject = models.BooleanField(default=False, verbose_name='是否展示在专题页面')

    class Meta:
        db_table = 'tb_nation'
        verbose_name = '地区'
        verbose_name_plural = '地区'

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=30, verbose_name="演员", unique=True)
    is_showon_subject = models.BooleanField(default=False, verbose_name='是否展示在专题页面')

    class Meta:
        db_table = 'tb_actor'
        verbose_name = '演员'
        verbose_name_plural = '演员'

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=60, verbose_name="导演", unique=True)
    is_showon_subject = models.BooleanField(default=False, verbose_name='是否展示在专题页面')

    class Meta:
        db_table = 'tb_director'
        verbose_name = '导演'
        verbose_name_plural = '导演'

    def __str__(self):
        return self.name


class Movie(models.Model):
    mname = models.CharField(max_length=100, verbose_name="电影名称", unique=True)
    mstory = RichTextUploadingField(verbose_name="电影简介")
    mimage = models.CharField(max_length=100, verbose_name="电影图片")
    mevaluate = models.FloatField(max_length=5, verbose_name="电影评价")
    mshowtime = models.DateField(verbose_name="上映时间")
    mclickcount = models.IntegerField(default=0, verbose_name="点击数量")
    mnation = models.ForeignKey(Nation, verbose_name='国家', on_delete=models.PROTECT, related_name='nation_movies')
    mdirector = models.ForeignKey(Director, verbose_name="导演", on_delete=models.PROTECT, related_name='actor_movies')
    create_time = models.DateField(verbose_name="创建时间")

    class Meta:
        db_table = 'tb_movie'
        verbose_name = '电影'
        verbose_name_plural = '电影'

    def __str__(self):
        return self.mname


class DownUrl(models.Model):
    url = models.CharField(max_length=100, verbose_name='下载链接', unique=True)
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, verbose_name='电影', related_name='down_urls')

    class Meta:
        db_table = 'tb_downurl'
        verbose_name = '电影对应的下载网址'
        verbose_name_plural = '电影对应的下载网址'

    def __str__(self):
        return self.url


class WatchUrl(models.Model):
    url = models.CharField(max_length=100, verbose_name='播放链接', unique=True)
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, verbose_name='电影', related_name='watch_urls')

    class Meta:
        db_table = 'tb_watchurl'
        verbose_name = '电影对应的观看网址'
        verbose_name_plural = '电影对应的观看网址'

    def __str__(self):
        return self.url


class CateGory(models.Model):
    cname = models.CharField(max_length=40, verbose_name="商品种类", unique=True)
    is_show = models.BooleanField(default=False, verbose_name='是否展示在搜索列表框')
    is_tag = models.BooleanField(default=False, verbose_name='是否展示在标签框')
    is_showon_subject = models.BooleanField(default=False, verbose_name='是否展示在专题页面')

    class Meta:
        db_table = 'tb_movie_category'
        verbose_name = '电影类型'
        verbose_name_plural = '电影类型'

    def __str__(self):
        return self.cname


class Connection_Movie_Category(models.Model):
    movie = models.ForeignKey(Movie, verbose_name='电影', on_delete=models.PROTECT, related_name='categorys')
    category = models.ForeignKey(CateGory, verbose_name='种类', on_delete=models.PROTECT, related_name='movies')

    class Meta:
        db_table = 'tb_connection_movie_category'
        verbose_name = '电影与类型的对应关系'
        verbose_name_plural = '电影与类型的对应关系'


class Connection_Movie_Actor(models.Model):
    movie = models.ForeignKey(Movie, verbose_name='电影', on_delete=models.PROTECT, related_name='actors')
    actor = models.ForeignKey(Actor, verbose_name='演员', on_delete=models.PROTECT, related_name='movies')

    class Meta:
        db_table = 'tb_connection_movie_actor'
        verbose_name = '电影与演员的对应关系'
        verbose_name_plural = '电影与演员的对应关系'
