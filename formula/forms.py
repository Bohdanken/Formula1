from django import forms
from django.contrib.auth.models import User
from formula.models import NAME_MAX_LENGTH, DESC_MAX_LENGTH, Post, Topic, UserProfile

class TopicForm(forms.ModelForm):
    name = forms.CharField(max_length=NAME_MAX_LENGTH,
                           help_text="Please enter the name of the topic.")
    description = forms.CharField(max_length=DESC_MAX_LENGTH,
                           help_text="Briefly describe this topic.")

    class Meta:
        model = Topic
        exclude = ('category','date_added',)



class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=NAME_MAX_LENGTH,
                           help_text="Please enter the post title.")
    description = forms.CharField(max_length=DESC_MAX_LENGTH,
                           help_text="Briefly describe your post.")
    content = forms.CharField(max_length=Post.CONTENT_MAX_LENGTH,
                           help_text="Write something here.")
    viewership = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Post
        exclude = ('topic','date_added',)



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',)



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user','is_admin',)