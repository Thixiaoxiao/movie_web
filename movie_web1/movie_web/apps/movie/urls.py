from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views

# urlpatterns 是被django自动识别的路由列表变量

urlpatterns = [
    url(r"^cates/$", views.CatesListView.as_view()),
    url(r"^cates/(?P<cate_id>\d+)/$", views.CateMovie.as_view()),
    url(r"^clickrank/$", views.ClickRankView.as_view()),
    url(r"^tags/$", views.TagsView.as_view()),
    url(r"^evaluate/$", views.EvaluateRankView.as_view()),
    url(r"^realtedmovie/cateid=(?P<cate_list_str>[0123456789-]+)/$", views.RelatedmovieView.as_view()),
    url(r"^querygetmovie/key=(?P<key>\w+)/id=(?P<id>\d+)/$", views.QueryMovieView.as_view()),
    url(r"^search/q=(?P<key>\w+)/$", views.SearchView.as_view()),
    url(r"^subjects/$", views.SubjectsGetView.as_view()),
    url(r"^areas/$", views.AreasView.as_view()),
    url(r"^evaluaterankmovielist/$", views.EvaluateRankMovieListView.as_view()),
    url(r"^inlandmovielist/$", views.InlandMovieListView.as_view()),
    url(r"^occmovielist/$", views.OccView.as_view()),
    url(r"^jpanhanmovielist/$", views.JpanhanMovieListView.as_view()),

]
router = DefaultRouter()  # 可以处理视图的路由器
router.register(r'movies', views.MovieView)  # 向路由器中注册视图集

urlpatterns += router.urls  # 将路由器中的所以路由信息追到到django的路由列表中
