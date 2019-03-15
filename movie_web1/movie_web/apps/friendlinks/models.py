from django.db import models


# Create your models here.
class FriendLink(models.Model):
    linkname = models.CharField(max_length=30, verbose_name='友情链接名称', unique=True)
    linkurl = models.CharField(max_length=100, verbose_name='友情链接地址', unique=True)

    class Meta:
        db_table = 'tb_friendlink'
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.linkname
