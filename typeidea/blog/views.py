from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from .models import Post, Tag, Category


# Create your views here.
def post_list(request, category_id=None, tag_id=None):  # 这里传进来的参数就是url中的正则表达式
    tag = None
    category = None

    if tag_id:
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
    else:
        post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                category = None
            else:
                post_list = post_list.filter(category_id=category_id)

    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
    }

    # content = 'post_list category_id={category_id},tag_id={tag_id}'.format(category_id=category_id,
    #                                                                        tag_id=tag_id)  # 这里一定要给出值传参,
    return render(request, 'blog/list.html', context=context)  # 这里的request封装了HTTP的请求


def post_detail(request, post_id=None):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    return render(request, 'blog/detail.html', context={'post': post})
