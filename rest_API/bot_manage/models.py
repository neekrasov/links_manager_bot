from django.db import models


class User(models.Model):
    chat_id = models.BigIntegerField(primary_key=True, verbose_name='ID')
    full_name = models.CharField(verbose_name='Full name', max_length=64)
    username = models.CharField(verbose_name='Username', max_length=32)

    def __str__(self):
        return f'{self.chat_id}:{self.full_name}'

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Group(models.Model):
    chat_id = models.BigIntegerField(primary_key=True, verbose_name='ID')
    title = models.CharField(verbose_name='Title', max_length=64)

    def __str__(self):
        return f'{self.chat_id}:{self.title}'

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"


class GroupUsers(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    group_id = models.ForeignKey(Group, verbose_name='Group ID', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, verbose_name='Group ID', on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.group_id}:{self.user_id}'

    class Meta:
        verbose_name = "Group User"
        verbose_name_plural = "Groups Users"


class Link(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    group_id = models.ForeignKey(Group, verbose_name='Group ID', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Title', max_length=64)
    url = models.URLField(verbose_name="URL")
    one_time = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}:{self.group_id}'

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"


class DateTimeForLink(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    link_id = models.ForeignKey(Link, verbose_name="Link ID", on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Date')
    time_start = models.TimeField(verbose_name='Time Start')
    time_finish = models.TimeField(verbose_name='Time Finish')
    repeat = models.IntegerField(verbose_name='Repeat')

    def __str__(self):
        return f'link_id:{self.link_id}'

    class Meta:
        verbose_name = "Date and Time for Link"
        verbose_name_plural = "Date and Time for Links"
