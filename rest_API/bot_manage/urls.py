from django.urls import path, register_converter
from rest_framework.urlpatterns import format_suffix_patterns
from . import views, service

"""USER"""
users_list = views.UserViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
groups_for_user_list = views.GroupUsersViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

"""GROUP"""
groups_list = views.GroupViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
links_for_group_list = views.LinksForGroupViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
# links_datetime_for_group_list = views.DateTimeForLinkViewSet.as_view({
#     'get': 'list',
#     'post': 'create',
# })

"""LINKS"""
links_list = views.LinkViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
links_datetime_list = views.DateTimeForLinkViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

register_converter(service.NegativeIntConverter, 'negint')
urlpatterns = format_suffix_patterns([

    path("users/", users_list),
    path("users/<negint:pk>", views.UserViewSet.as_view({'get': 'retrieve'})),
    path("users/<negint:user_id>/groups", groups_for_user_list),

    path("groups/", groups_list),
    path("groups/<negint:pk>", views.GroupViewSet.as_view({'get': 'retrieve'})),
    path("groups/<negint:group_id>/links", links_for_group_list),
    # path("groups/<negint:group_id>/links/datetime", links_datetime_for_group_list),

    path("links/", links_list),
    path("links/datetime", links_datetime_list),
    path("links/<int:pk>", views.LinkViewSet.as_view({'get': 'retrieve'})),
    path("links/<int:link_id>/datetime", views.DateTimeForLinkViewSet.as_view({'get': 'list'})),

])
