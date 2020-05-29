from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment
from .forms import CommentForm
from django.template.loader import render_to_string
from django_ajax.decorators import ajax
from django.views.decorators.csrf import csrf_protect
from taggit.models import Tag
from django.template import Variable, VariableDoesNotExist
from django.core.paginator import Paginator


def home(request):
    context = {
        'posts': Post.objects.order_by('-posted_on')[:3]
    }
    return render(request, 'writeups/home.html', context)


def about(request):
    return render(request, 'writeups/about.html')


def blogs(request):

    posts = Post.objects.order_by('-posted_on')
    tags = Post.tags.most_common()[:5]
    paginator = Paginator(posts, 5)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    colors = [
        'primary',
        'secondary',
        'success',
        'danger',
        'warning',
        'info',
        'light',
        'dark'
    ]

    context = {
        'posts': posts,
        'tags': tags,
        'colors': colors,
        'page': page
    }

    return render(request, 'writeups/blogs.html', context)


def detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    is_liked = False

    if post.like.filter(id=request.user.id).exists():
        is_liked = True

    if request.method == 'POST':

        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():

            content = request.POST.get('text')
            reply_id = request.POST.get('comment_id')
            comment_qs = None

            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)

            comment = Comment.objects.create(
                post=post, user=request.user, text=content, reply=comment_qs)
            comment.save()

            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'is_liked': is_liked,
        'comments': comments,
        'likes': post.like.count(),
        'comment_form': comment_form
    }

    return render(request, 'writeups/detail.html', context)


# @ajax
# @csrf_protect
@login_required(login_url='/accounts/login/')
def like(request, id, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = False

    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
    else:
        post.like.add(request.user)
        is_liked = True

    context = {
        'post': post,
        'is_liked': is_liked,
        'likes': post.like.count()
    }

    if request.is_ajax():
        html = render_to_string(
            'writeups/like_section.html', context, request=request)
        return JsonResponse({'form': html})
    else:
        return HttpResponseRedirect(post.get_absolute_url())


@login_required(login_url='/accounts/login/')
def profile(request):
    return render(request, 'account/profile.html')
