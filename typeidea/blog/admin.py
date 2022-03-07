from django.contrib.admin.models import LogEntry
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin


# Register your models here.


class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1  # 控制额外多几个
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')
    inlines = [PostInline, ]

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator'
    ]  # 列表页面展示哪些字段
    list_display_links = []  # 用来展示哪些字段可以作为链接

    list_filter = [CategoryOwnerFilter]  # 需要通过哪些字段来过滤列表页,这里使用了上面自定义的分类过滤器
    search_fields = ['title', 'category__name']  # 配置搜索字段

    actions_on_top = True  # 动作相关的配置,是否展示在顶部
    actions_on_bottom = True

    save_on_top = True  # 保存,编辑,编辑并新建按钮是否在顶部显示
    exclude = ('owner',)  # 不需要展示的字段

    # fields = (  # 限定要展示的字段并且可以配置展示字段的顺序
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        (
            '额外信息', {
                'classes': ('collapse',),
                'fields': ('tag',),
            })
    )
    filter_horizontal = ('tag',)  # 设置横向展示的字段

    # filter_vertical = ('tag',) # 设置纵向展示的字段

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    # class Media:
    #     css = {
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
    #     }
    #     js = 'https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'
    class Media:
        css = {
            'all': ("https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap.min.css",), }
        js = ("https://cdn.bootcss.com/twitter-bootstrap/4.4.0/js/bootstrap.bundle.js",)


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user',
                    'change_message']
