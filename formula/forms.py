from django import forms
from django.contrib.auth.models import User
from formula.models import NAME_MAX_LENGTH, DESC_MAX_LENGTH, Post, Topic, UserProfile

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=NAME_MAX_LENGTH,
                           help_text="Please enter the post title.")
    description = forms.CharField(max_length=DESC_MAX_LENGTH,
                           help_text="Briefly describe your post.")
    content = forms.CharField(max_length=Post.CONTENT_MAX_LENGTH,
                           help_text="Write something here.")
    #file = forms.FileField(max_length=Post.FILES_MAX_LENGTH)
    viewership = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    author = forms.IntegerField(widget=forms.HiddenInput())
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Post
        exclude = ('date_added',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user','admin',)