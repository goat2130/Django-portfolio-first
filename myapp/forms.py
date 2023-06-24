from django import forms
from .models import Post, Comment, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# post
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content')

# signup
class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'created_date', 'approved_comment')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'website', 'location', 'avatar', 'experience')
