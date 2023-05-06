from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Profile, PostViews
from .forms import PostForm, ProfileForm, SignUpForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth import login
from django.utils import timezone
from django_comments.models import Comment
from django.db.models import F, Count
from django.http import HttpResponseRedirect
from django.views.generic import CreateView




# Post Function
def post_list(request):
    posts = Post.objects.all()
    ranked_posts = Post.objects.annotate(num_views=F('views') + 1).order_by('-num_views')[:5]

    # コメントのフォームの処理
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post
            comment.save()
            return redirect('post_detail', pk=Post.pk)
    else:
        form = CommentForm()

    return render(request, 'myapp/post_list.html', {'posts': posts, 'ranked_posts': ranked_posts, 'form': form})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # ログインしているユーザーを投稿のauthorに設定する
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'myapp/post_form.html', {'form': form})


# def post_detail(request, pk):
#    post = get_object_or_404(Post, pk=pk)
#    return render(request, 'myapp/post_detail.html', {'post': post})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')



# login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', pk=pk)

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


# Comment Function
from .forms import CommentForm

def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    comments = post.comments.filter(approved_comment=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'myapp/post_detail.html', {'post': post, 'form': form, 'comments': comments})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'myapp/post_edit.html', {'form': form})
from django.utils import timezone

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.created_date = timezone.now() # 現在の日時をセットする
            comment.save()
            return redirect(reverse('post_detail', kwargs={'pk': post.pk}))
    else:
        form = CommentForm()
    return render(request, 'myapp/add_comment_to_post.html', {'form': form, 'post': post})

# profile_function
def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    if profile is None:
        profile = Profile(user=request.user)
        profile.save()

    context = {
        'form': form,
        'profile': profile
    }

    return render(request, 'myapp/profile.html', context)

# ranking function
def increment_views(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.views += 1
    post.save()
    post_views, created = PostViews.objects.get_or_create(post=post)
    post_views.views_count += 1
    post_views.save()
    ranked_posts = Post.objects.order_by('-views')[:5]
    return render(request, 'myapp/post_detail.html', {'post': post, 'ranked_posts': ranked_posts})



def ranking(request):
    posts = Post.objects.annotate(view_count=Count('views')).order_by('-view_count')[:10]
    return render(request, 'ranking.html', {'posts': posts})

def ranking_view(request):
    ranked_posts = Post.objects.order_by('-views')[:10]
    return render(request, 'myapp/ranking.html', {'ranked_posts': ranked_posts})

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
