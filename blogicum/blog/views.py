from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from . import constants
from .models import Category, Post


def filter_published_posts(queryset):
    return queryset.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    ).select_related(
        'author',
        'location',
        'category',
    )


def index(request):
    post_list = filter_published_posts(Post.objects)[:constants.POSTS_LIMIT]

    return render(
        request,
        'blog/index.html',
        {'post_list': post_list},
    )


def post_detail(request, post_id):
    post = get_object_or_404(
        filter_published_posts(Post.objects),
        pk=post_id,
    )

    return render(
        request,
        'blog/detail.html',
        {'post': post},
    )


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )

    post_list = filter_published_posts(category.posts)

    return render(
        request,
        'blog/category.html',
        {
            'category': category,
            'post_list': post_list,
        },
    )
