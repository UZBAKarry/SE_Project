from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
import markdown
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model as user_model
from django.core.validators import MinLengthValidator
User1 = user_model()
# from django.utils.functional import cached_property
# from markdown.extensions.toc import TocExtension
# from django.utils.text import slugify


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    members = models.ManyToManyField(User, through='MemberShip')
    views = models.PositiveIntegerField(default=0, blank=True, null=True)
    description = models.TextField(default="")

    class Meta:
        verbose_name = '小组'
        verbose_name_plural = verbose_name

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('group_func:group_detail', kwargs={'pk': self.pk})

    def get_group(self):
        return reverse('group_func:group_detail', kwargs={'pk': self.pk})


class MemberShip(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_join = models.DateTimeField()

    class Meta:
        verbose_name = '小组关系'


class GroupPost(models.Model):
    title = models.CharField('标题', max_length=70)
    body = models.TextField(validators=[MinLengthValidator(25)])
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')
    excerpt = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(User, verbose_name='作者', null=True, on_delete=models.CASCADE, )
    views = models.PositiveIntegerField(default=0, blank=True, null=True)
    group = models.ForeignKey(Group, verbose_name='小组名', related_name='grouptalk', on_delete=models.CASCADE)
    top = models.BooleanField(default=False)
    top_time = models.DateTimeField('置顶时间', default=timezone.now)
    im = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        verbose_name = '小组讨论'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
        default_permissions = ()
        permissions = (
            ("grouppost_delete", "讨论删除权限"),)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('group_func:group_detailmore', kwargs={'pk': self.group.pk})
