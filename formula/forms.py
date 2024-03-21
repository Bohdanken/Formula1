from django import forms

from formula.models import *
from formula.fields import *

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


