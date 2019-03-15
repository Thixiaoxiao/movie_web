from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from movie.models import Movie, CateGory


class MovieSerializer(ModelSerializer):
    """电影序列化器"""

    class Meta:
        model = Movie
        fields = ('id', 'mname', 'mimage', 'mevaluate','mshowtime')


class MovieRectriveSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'mname','mnation','categorys','mdirector','watch_urls', 'mimage','down_urls' ,'mevaluate','mshowtime','actors','mstory')


class CatesLiseSerializer(ModelSerializer):
    class Meta:
        model = CateGory
        fields = ('id','cname')
