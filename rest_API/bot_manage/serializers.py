from rest_framework import serializers
from .models import User, Group, GroupUsers, Link, DateTimeForLink


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'chat_id',
            'full_name',
            'username',
        )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'chat_id',
            'title',
        )


class GroupUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupUsers
        fields = (
            'id',
            'group_id',
            'user_id',
            'is_admin',
        )


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = (
            'id',
            'group_id',
            'title',
            'url',
            'one_time',
        )


class DateTimeForLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateTimeForLink
        fields = (
            'id',
            'link_id',
            'date',
            'time_start',
            'time_finish',
            'repeat',
        )
