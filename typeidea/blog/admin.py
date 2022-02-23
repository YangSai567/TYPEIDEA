from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Post, Category, Tag


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)
        # 首先找到CategoryAdmin的父类,也就是ModelAdmin
        # 然后把CategoryAdmin的对象转换为ModelAdmin的对象
        # 然后执行ModelAdmin的savemodel方法

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator'
    ]  # 列表页面展示哪些字段
    list_display_links = []  # 用来展示哪些字段可以作为链接

    list_filter = ['category']  # 需要通过哪些字段来过滤列表页
    search_fields = ['title', 'category__name']  # 配置搜索字段

    actions_on_top = True  # 动作相关的配置,是否展示在顶部
    actions_on_bottom = True

    save_on_top = True  # 保存,编辑,编辑并新建按钮是否在顶部显示

    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)
