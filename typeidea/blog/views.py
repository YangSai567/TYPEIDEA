from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def post_list(request, category_id=None, tag_id=None):  # 这里传进来的参数就是url中的正则表达式
    content = 'post_list category_id={category_id},tag_id={tag_id}'.format(category_id=category_id,
                                                                           tag_id=tag_id)  # 这里一定要给出值传参,
    return render(request, 'blog/list.html', context={'name': 'post_list'})  # 这里的request封装了HTTP的请求


def post_detail(request, post_id):
    return render(request, 'blog/detail.html', context={'name': 'post_detail'})
