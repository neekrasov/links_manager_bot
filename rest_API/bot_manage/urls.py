from django.urls import path, register_converter
from rest_framework.urlpatterns import format_suffix_patterns
from . import views, service

users_list = views.UserViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
groups_list = views.GroupViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
groupusers_list = views.GroupUsersViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
link_list = views.LinkViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
datetimeforlink_list = views.DateTimeForLinkViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

register_converter(service.NegativeIntConverter, 'negint')
urlpatterns = format_suffix_patterns([

    path("users/", users_list),
    path("users/<negint:pk>", views.UserViewSet.as_view({'get': 'retrieve'})),
    path("groups/", groups_list),
    path("groups/<negint:pk>", views.GroupViewSet.as_view({'get': 'retrieve'})),
    path("groups/users/", groupusers_list),
    path("groups/users/<int:user_id>", views.GroupUsersViewSet.as_view({'get': 'list'})),
    path("links/", link_list),
    path("links/<int:pk>", views.LinkViewSet.as_view({'get': 'retrieve'})),
    path("links/group/<negint:group_id>", views.LinksForGroupViewSet.as_view({'get': 'list'})),
    path("links/datetime/", datetimeforlink_list),
    path("links/datetime/<int:link_id>", views.DateTimeForLinkViewSet.as_view({'get': 'list'})),

])
