from django.conf.urls import url

from . import views

# urlpatterns 是被django自动识别的路由列表变量

urlpatterns = [

    url(r"^friendlink/$", views.FriendLinkView.as_view()),

]

