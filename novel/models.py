import datetime

from django.db import models


class Chaptername(models.Model):
    id = models.AutoField(primary_key=True)
    xs_chaptername = models.CharField(max_length=255, verbose_name="章节名")
    xs_content = models.TextField(verbose_name="内容")
    id_name = models.CharField(max_length=15, verbose_name="书编号")
    num_id  = models.IntegerField(verbose_name="章节号")
    url = models.CharField(max_length=255, verbose_name="获取URL")
    prev = models.IntegerField(default=0, blank=True, null=True, verbose_name="上一章")
    next = models.IntegerField(default=0, blank=True, null=True, verbose_name="下一章")
    def __str__(self):
        return self.xs_chaptername
    class Meta:
        # abstract = True
        ordering = ['num_id']
        verbose_name='小说章节'
        verbose_name_plural=verbose_name

class Name(models.Model):
    id = models.AutoField(primary_key=True)
    xs_name = models.CharField(max_length=255, verbose_name="小说名")
    xs_author = models.CharField(max_length=255, verbose_name="作者")
    category = models.CharField(max_length=255, verbose_name="类别")
    name_id = models.CharField(max_length=255, verbose_name="书编号", unique=True)
    allrank = models.IntegerField(blank=True, null=True, default=0, verbose_name="总榜")
    monthrank = models.IntegerField(blank=True, null=True, default=0, verbose_name="月榜")
    weekrank = models.IntegerField(blank=True, null=True, default=0, verbose_name="周榜")
    summery = models.CharField(blank=True, null=True, max_length=500, verbose_name="简介")
    pic = models.CharField(blank=True, null=True, max_length=255, verbose_name="图片")
    def __str__(self):
        return self.xs_name
    class Meta:
        verbose_name='小说'
        verbose_name_plural=verbose_name

class Websetting(models.Model):
    name     = models.CharField(max_length=128, verbose_name="名称")
    key      = models.CharField(max_length=128, unique=True, verbose_name="key") # unique one
    value    = models.CharField(max_length=128, verbose_name="路径")
    url      = models.CharField(max_length=255, verbose_name="跳转URL", default="{% url 'novel:index' %}")
    time     = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name="上次修改时间")
    class Meta:
        verbose_name='网站设置'
        verbose_name_plural=verbose_name
