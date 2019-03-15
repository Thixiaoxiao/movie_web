from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView

# 友情链接处理视图
from friendlinks.models import FriendLink
from friendlinks.serializers import FriendLinkSerializer


class FriendLinkView(ListAPIView):
    """类视图处理"""
    queryset = FriendLink.objects.all()
    serializer_class = FriendLinkSerializer