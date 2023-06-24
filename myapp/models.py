from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import HttpRequest

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', blank=True)
    views = models.IntegerField(default=0)
    icon = models.ImageField(upload_to='icons/', blank=True, null=True)

    def get_rank(self):
        rank = 0
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-views', '-published_date')
        for i, post in enumerate(posts):
            if post == self:
                rank = i + 1
                break
        return rank

    def get_author_avatar_url(self):
        return self.author.profile.avatar.url if self.author.profile.avatar else None

    def __str__(self):
        return self.title

class Profile(models.Model):
    EXPERIENCE_CHOICES = [
        ('未経験', '未経験'),
        ('経験者', '経験者'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    website = models.URLField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    followers_count = models.PositiveIntegerField(default=0)
    experience = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES, default='未経験')

    def __str__(self):
        return self.user.username





class Comment(models.Model):
    post = models.ForeignKey('myapp.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def save(self, *args, **kwargs):
        if not self.pk and not self.author_id:
            # 新しいコメントで、まだauthorが設定されていない場合
            self.author = self._get_current_user()
        super().save(*args, **kwargs)

    def _get_current_user(self):
        from django.contrib.auth.models import AnonymousUser
        from django.contrib.sessions.middleware import SessionMiddleware
        from django.contrib.auth.middleware import get_user

        # ダミーリクエストオブジェクトを作成し、セッションと認証情報を設定します
        request = HttpRequest()
        SessionMiddleware().process_request(request)
        request.session.save()

        # リクエストから現在のユーザーを取得します
        user = request.user

        if user.is_authenticated:
            return user
        else:
            return AnonymousUser()

    def __str__(self):
        return self.text


class PostViews(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_views')
    views_count = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.post) + ' views'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.post.slug})


class Connection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='followers', blank=True)
    def __str__(self):
        return self.user.username
