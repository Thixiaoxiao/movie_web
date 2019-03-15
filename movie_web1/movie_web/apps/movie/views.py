from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from movie.models import Movie, CateGory, Connection_Movie_Category, Actor, DownUrl, WatchUrl, Nation, \
    Connection_Movie_Actor, Director
from movie.serializers import MovieSerializer, MovieRectriveSerializer, CatesLiseSerializer

num_map = {
    1:  '一',
    2:  '二',
    3:  '三',
    4:  '四',
    5:  '五',
    6:  '六',
    7:  '七',
    8:  '八',
    9:  '九',
    10: '十'
}


class LargeResultsSetPagination(PageNumberPagination):
    # 电影列表控制
    page_size = 16
    page_size_query_param = 'page_size'
    max_page_size = 40


class ClickRankSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 16


class EvaluateRankSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 16


# 电影推送
class RelatedMovieSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 16


# GET movies/id
class MovieView(ReadOnlyModelViewSet):
    queryset = Movie.objects.all().order_by('-create_time')
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        # 序列化
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.mclickcount += 1
        instance.save()
        serializer = self.get_serializer(instance)
        response_data = serializer.data
        actors_list = []
        for item in response_data['actors']:
            new_dict = {}
            actobj = Connection_Movie_Actor.objects.get(id=item).actor

            new_dict['id'] = actobj.id
            new_dict['name'] = actobj.name
            new_dict['url_link'] = 'querygetmovie.html?key=%s&id=%s' % ('actors', actobj.id)
            actors_list.append(new_dict)
        response_data['actors'] = actors_list
        down_urls = []
        for index, item in enumerate(response_data['down_urls']):
            new_dict = {}
            new_dict['ikn'] = '下载地址:' + num_map[index + 1]
            new_dict['contents'] = DownUrl.objects.get(id=item).url
            down_urls.append(new_dict)
        response_data['down_urls'] = down_urls
        watch_urls = []
        for index, item in enumerate(response_data['watch_urls']):
            new_dict = {}
            new_dict['ikn'] = '播放地址:' + num_map[index + 1]
            new_dict['contents'] = WatchUrl.objects.get(id=item).url
            watch_urls.append(new_dict)
        response_data['watch_urls'] = watch_urls
        cate_list = []
        for item in response_data['categorys']:
            new_dict = {}
            cateobj = Connection_Movie_Category.objects.get(id=item).category
            new_dict['cate_id'] = cateobj.id
            new_dict['cname'] = cateobj.cname
            new_dict['cate_url'] = 'querygetmovie.html?key=%s&id=%s' % ('categorys', cateobj.id)
            cate_list.append(new_dict)
        response_data['categorys'] = cate_list
        mnation_dict = {}
        n_id = response_data['mnation']
        mnation_dict['name'] = Nation.objects.get(id=n_id).name
        mnation_dict['nation_url'] = 'querygetmovie.html?key=%s&id=%s' % ('mnation', n_id)
        response_data['mnation'] = mnation_dict
        mdirector_dict = {}
        d_id = response_data['mdirector']
        mdirector_dict['name'] = Director.objects.get(id=d_id).name
        mdirector_dict['director_url'] = 'querygetmovie.html?key=%s&id=%s' % ('mdirector', d_id)
        response_data['mdirector'] = mdirector_dict
        return Response(response_data)

    def get_serializer_class(self):
        return MovieSerializer if self.action == 'list' else MovieRectriveSerializer


class CatesListView(ListAPIView):
    """电影的种类视图处理"""
    queryset = CateGory.objects.filter(is_show=True).order_by('id')
    serializer_class = CatesLiseSerializer


# 获取某一类电影
class CateMovie(ListAPIView):
    serializer_class = MovieSerializer
    pagination_class = LargeResultsSetPagination
    ordering_fields = ('create_time',)

    def get_queryset(self):
        queryset = Connection_Movie_Category.objects.filter(category_id=self.kwargs['cate_id'])
        movie_id_list = [item.movie.id for item in queryset]
        return Movie.objects.filter(id__in=movie_id_list)


class ClickRankView(ListAPIView):
    """点击量排行 """
    queryset = Movie.objects.all().order_by('-mclickcount')
    serializer_class = MovieSerializer
    pagination_class = ClickRankSetPagination


class TagsView(ListAPIView):
    """获取标签 视图类"""
    queryset = CateGory.objects.filter(is_tag=True).order_by('id')
    serializer_class = CatesLiseSerializer


class EvaluateRankView(ListAPIView):
    """评价排行电影列表视图类处理"""
    queryset = Movie.objects.all().order_by('-mevaluate')
    serializer_class = MovieSerializer
    pagination_class = EvaluateRankSetPagination


# GET /realtedmovie/cateid=1-2/
class RelatedmovieView(ListAPIView):
    """电影推送 类视图 """
    serializer_class = MovieSerializer
    pagination_class = RelatedMovieSetPagination

    def get_queryset(self):
        cate_list_str = self.kwargs['cate_list_str']
        cate_list = cate_list_str.split('-')  # [3,4]
        movie_list = [item.movie.id for item in Connection_Movie_Category.objects.filter(category__in=cate_list)]
        return Movie.objects.filter(id__in=movie_list).order_by('mclickcount')


# GET /querygetmovie/key=actor/id=46/
class QueryMovieView(ListAPIView):
    """类视图处理"""
    pagination_class = LargeResultsSetPagination
    serializer_class = MovieSerializer

    def get_queryset(self):
        if self.kwargs['key'] == 'actors':
            movie_id_list = [item.movie.id for item in Connection_Movie_Actor.objects.filter(actor=self.kwargs['id'])]
            return Movie.objects.filter(id__in=movie_id_list)
        elif self.kwargs['key'] == 'mnation':
            return Movie.objects.filter(mnation=self.kwargs['id'])


        elif self.kwargs['key'] == 'categorys':
            movie_id_list = [item.movie.id for item in
                             Connection_Movie_Category.objects.filter(category=self.kwargs['id'])]
            return Movie.objects.filter(id__in=movie_id_list)

        elif self.kwargs['key'] == 'mdirector':
            return Movie.objects.filter(mdirector=self.kwargs['id'])


# GET /search/q=你好/
class SearchView(ListAPIView):
    """类视图处理"""
    pagination_class = LargeResultsSetPagination
    serializer_class = MovieSerializer

    def get_queryset(self):
        key = self.kwargs['key']
        # print(key)
        movie_id_list = []
        movie_id_list.extend([item.id for item in Movie.objects.filter(mname__contains=key)])
        nation_id_list = [item.id for item in Nation.objects.filter(name__contains=key)]
        movie_id_list.extend([item.id for item in Movie.objects.filter(mnation__in=nation_id_list)])
        # 演员
        actor_id_list = [item.id for item in Actor.objects.filter(name__contains=key)]
        movie_id_list.extend([item.movie.id for item in Connection_Movie_Actor.objects.filter(actor__in=actor_id_list)])

        # 种类
        cate_id_list = [item.id for item in CateGory.objects.filter(cname__contains=key)]
        movie_id_list.extend(
            [item.movie.id for item in Connection_Movie_Category.objects.filter(category__in=cate_id_list)])
        # 导演
        director_id_list = [item.id for item in Director.objects.filter(name__contains=key)]
        movie_id_list.extend([item.id for item in Movie.objects.filter(mdirector__in=director_id_list)])

        movie_id_list = list(set(movie_id_list))
        return Movie.objects.filter(id__in=movie_id_list)


# GET /subjects/
class SubjectsGetView(APIView):
    """类视图处理"""

    def get(self, request):
        """处理--GET--方式的请求"""
        response_list = [
            {
                'key':      'actors',
                'namelist': [{'id': item.id, 'name': item.name} for item in
                             Actor.objects.filter(is_showon_subject=True)]
            },
            {
                'key':      'mnation',
                'namelist': [{'id': item.id, 'name': item.name} for item in
                             Nation.objects.filter(is_showon_subject=True)]

            },
            {
                'key':      'mdirector',
                'namelist': [{'id': item.id, 'name': item.name} for item in
                             Director.objects.filter(is_showon_subject=True)]

            },
            {
                'key':      'categorys',
                'namelist': [{'id': item.id, 'name': item.cname} for item in
                             CateGory.objects.filter(is_showon_subject=True)]

            }
        ]

        return Response(response_list)


# GET /areas/
class AreasView(APIView):
    """地区视图处理"""

    def get(self, request):
        """处理--GET--方式的请求"""

        return Response([{
            'key':      'mnation',
            'namelist': [{'id': item.id, 'name': item.name} for item in
                         Nation.objects.all()]

        }])


# GET /evaluaterankmovielist/
class EvaluateRankMovieListView(ListAPIView):
    """类视图处理"""
    queryset = Movie.objects.filter(mevaluate__gt=8).order_by('-mevaluate')
    serializer_class = MovieSerializer
    pagination_class = LargeResultsSetPagination


# GET /inlandmovielist/
class InlandMovieListView(ListAPIView):
    """类视图处理"""
    serializer_class = MovieSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        nation_id_list = []
        nation_id_list.extend([item.id for item in Nation.objects.filter(name__contains='中国')])
        nation_id_list.extend([item.id for item in Nation.objects.filter(name__contains='大陆')])
        nation_id_list = list(set(nation_id_list))
        return Movie.objects.filter(mnation__in=nation_id_list)


# GET /occmovielist/
class OccView(ListAPIView):
    """类视图处理"""
    serializer_class = MovieSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        nation_id_list = []
        nation_id_list.extend([item.id for item in Nation.objects.filter(name__contains='美国')])
        nation_id_list.extend([item.id for item in Nation.objects.filter(name__contains='英国')])
        nation_id_list = list(set(nation_id_list))
        return Movie.objects.filter(mnation__in=nation_id_list)


# GET /jpanhanmovielist/
class JpanhanMovieListView(ListAPIView):
    """类视图处理"""
    serializer_class = MovieSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        nation_id_list = []
        nation_id_list.extend([item.id for item in Nation.objects.filter(name__contains='韩国')])
        nation_id_list.extend([item.id for item in Nation.objects.filter(name__contains='日本')])
        nation_id_list = list(set(nation_id_list))
        return Movie.objects.filter(mnation__in=nation_id_list)
