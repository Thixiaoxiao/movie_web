import xadmin
from xadmin import views

from friendlinks.models import FriendLink
from . import models


class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "电影资源管理系统"  # 设置站点标题
    site_footer = "晨曦遇晓"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠


xadmin.site.register(views.CommAdminView, GlobalSettings)


class MovieAdmin(object):
    model_icon = 'fa fa-gift'


xadmin.site.register(models.Movie, MovieAdmin)
xadmin.site.register(models.Connection_Movie_Actor)
xadmin.site.register(models.Connection_Movie_Category)
xadmin.site.register(models.CateGory)
xadmin.site.register(models.Nation)
xadmin.site.register(models.Actor)
xadmin.site.register(models.Director)
xadmin.site.register(FriendLink)
