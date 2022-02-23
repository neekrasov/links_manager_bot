from rest_framework.viewsets import ViewSet, ModelViewSet

from .models import User, Group, GroupUsers, Link, DateTimeForLink
from .serializers import UserSerializer, GroupSerializer, GroupUsersSerializer, LinkSerializer, \
    DateTimeForLinkSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class GroupViewSet(ModelViewSet):
    serializer_class = GroupSerializer

    def get_queryset(self):
        return Group.objects.all()


class GroupUsersViewSet(ModelViewSet):
    serializer_class = GroupUsersSerializer
    lookup_field = 'user_id'

    def get_queryset(self):
        return GroupUsers.objects.all()


class LinkViewSet(ModelViewSet):
    serializer_class = LinkSerializer

    def get_queryset(self):
        return Link.objects.all()


class LinksForGroupViewSet(ModelViewSet):
    serializer_class = LinkSerializer
    lookup_field = 'group_id'

    def get_queryset(self):
        return Link.objects.all()


class DateTimeForLinkViewSet(ModelViewSet):
    serializer_class = DateTimeForLinkSerializer
    lookup_field = 'link_id'

    def get_queryset(self):
        return DateTimeForLink.objects.all()
