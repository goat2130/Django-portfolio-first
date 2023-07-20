from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import HttpRequest

"""
models.pyはデータベースとの連携を行います。検索、取得、追加、削除の一連の流れが行うことができます。
urlsルーティングとview.pyから、データのリクエストを受け取りそのリクエストに沿ってデータの受け渡しをします。
またDjangoでは、モデルを使うことでSQL文を使わないでデータベース操作を可能とします

"""
class Post(models.Model):
    title = models.CharField(max_length=200) #２００文字まで取得
    content = models.TextField() #長いテキストデータを取得
    author = models.ForeignKey(User, on_delete=models.CASCADE) #userと紐付け、紐づけたuserが消えた場合には投稿も削除
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', blank=True) # 多対多でデータを持つ
    views = models.IntegerField(default=0) #閲覧数
    icon = models.ImageField(upload_to='icons/', blank=True, null=True) #画像を取得、見れる

    def get_rank(self): #投稿ランキング機能
        rank = 0 #初期化
        # post一覧から現在の時刻より前の投稿を取得し、閲覧数の多い順と公開日の新しい物いから順位表示する
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-views', '-published_date')
        for i, post in enumerate(posts): #enumerateを使ってindex,postを取得。ランク変数にindexを１ずつ増やして格納
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

    user = models.OneToOneField(User, on_delete=models.CASCADE) #1対１でデータを持つ
    bio = models.TextField(max_length=500, blank=True) #長いテキストデータを取得
    website = models.URLField(max_length=200, blank=True) #"url型でデータを保持"
    location = models.CharField(max_length=100, blank=True)# 文字データを取得
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)# 画像データを取得、リンクはavatars/
    followers = models.ManyToManyField(User, related_name='following', blank=True)# 多対多のデータを持つ
    followers_count = models.PositiveIntegerField(default=0)# 整数型で整数のみのデータを持つ
    experience = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES, default='未経験')# choicesから未経験か経験者かを選ぶことができる

    def __str__(self):
        return self.user.username





class Comment(models.Model):
    post = models.ForeignKey('myapp.Post', on_delete=models.CASCADE, related_name='comments')# myapp.postに１対多の形でコメントのデータが持てるようにする
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)# custom user default user などの使用モデルを問わず、現在使用しているuserモデルを返す
    text = models.TextField()# text date
    created_date = models.DateTimeField(default=timezone.now)# コメントをした日時を自動で設定
    approved_comment = models.BooleanField(default=False)# チェックを入れることでつまりTRUE

    def approve(self):
        self.approved_comment = True
        self.save() # True でコメントを保存

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
            return AnonymousUser()# ログインしていないと返す

    def __str__(self):
        return self.text


class PostViews(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_views')# post を１対他でもてるよう設定
    views_count = models.IntegerField(default=0)# 閲覧数をカウントする。ランキング機能の要
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.post) + ' views'# 管理画面でデータの判別をしやすいようstrを指定する。こちらはそれぞれの投稿と閲覧数を設定する

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.post.slug})


class Connection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)# 1 : 1でデータを持つように設定
    following = models.ManyToManyField(User, related_name='followers', blank=True)# 多　対　多でもちフォロワーの数を設定
    def __str__(self):
        return self.user.username
