import requests
import urllib
from django.http import HttpResponse
from .dataSite import start_Url_code, start_Url_access_token, start_request_API
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

'''client_id = '7021952'                                      
client_secret = 'stIHRvDcAxhPTA4WO43g'                      
redirect_uri = 'https://serg666999.pythonanywhere.com'''

'''url = https://oauth.vk.com/authorize?client_id=7021952&display=page&redirect_uri=https://serg666999.pythonanywhere.com&scope=friends&response_type=code&v=5.95'''

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            r=start_Url_code()
            r
            print(r)
            print(r.url)
            print('hello world')
            print(request.GET.get('code'))
            print(r.status_code)
            print(request.GET)
            return redirect(r.url, pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

def vk(request):
    r = start_Url_code()
    code = request.GET.get('code')
    r2 = start_Url_access_token(code)

    data_token = eval(r2.content)
    access_token = data_token.get('access_token')
    user_id = data_token.get('user_id')

    r3=start_request_API(access_token,user_id)

    print('url_code = ', r.url)
    print('url_token = ', r2.url)
    print('code = ', code)
    print(r2.content)
    print(r2.text)
    print('access_token = ', access_token, 'user_id = ', user_id)
    print('answer_API = ', r3.json())

    return render(request, 'blog/vkontakte.html', )
# Create your views here.

class MyRegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/accounts/login/"
    template_name = "registration/register.html"

    def form_valid(self, form):
        form.save()
        return super(MyRegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(MyRegisterFormView, self).form_invalid(form)