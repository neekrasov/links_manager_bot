from django.contrib import admin
from .models import User, Group, Link, GroupUsers, DateTimeForLink

admin.site.register(User)
admin.site.register(Group)
admin.site.register(Link)
admin.site.register(GroupUsers)
admin.site.register(DateTimeForLink)