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


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
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
            reverse('admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    # 使用户只能看到自己创建的文章
    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
