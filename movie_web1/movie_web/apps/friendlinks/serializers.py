from rest_framework.serializers import  ModelSerializer

from friendlinks.models import FriendLink


class FriendLinkSerializer(ModelSerializer):
    class Meta:
        model=FriendLink
        fields='__all__'




