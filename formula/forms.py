from django import forms

from formula.models import *
from formula.fields import *
from django.contrib.auth.forms import UserChangeForm

class TopicForm(forms.ModelForm):
    name = forms.CharField(max_length=NAME_MAX_LENGTH,
                           help_text="Please enter the name of the topic.")
    description = forms.CharField(max_length=DESC_MAX_LENGTH,

                                  help_text="Briefly describe this topic.",
                                  widget=forms.Textarea)

    class Meta:
        model = Topic
        exclude = ('slug','category', 'date_added',)


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=NAME_MAX_LENGTH,
                            help_text="Please enter the post title.")
    description = forms.CharField(max_length=DESC_MAX_LENGTH,
                                  help_text="Briefly describe your post.")
    content = forms.CharField(max_length=Post.CONTENT_MAX_LENGTH,
                              help_text="Write something here.",
                              widget=forms.Textarea)
    file = MultipleFileField(required=False)

    

    class Meta:
        model = Post
        exclude = ('topic', 'date_added', 'viewership', 'author')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'first_name', 'last_name','student_id','picture','bio')


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'bio', 'picture')

class EditProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False, help_text='Enter a new password or leave blank to keep the current one.')
    picture = forms.ImageField(required=False, help_text='Select a new profile picture or leave blank to keep the current one.')
    bio = forms.CharField(widget=forms.Textarea, required=False, help_text='Update your bio.')

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'bio', 'picture')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            return self.initial["password"]
        return password




