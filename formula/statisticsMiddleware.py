
from django.utils.deprecation import MiddlewareMixin
from formula.models import Post, Topic, CustomUser
from django.shortcuts import render

class StatisticsMiddleware(MiddlewareMixin):
    def statistics_processor(request):
        total_posts = Post.objects.count()
        total_topics = Topic.objects.count()
        total_members = CustomUser.objects.count()
        newest_member = CustomUser.objects.latest('date_joined')

        context_dict = {
            'total_posts': total_posts,
            'total_topics': total_topics,
            'total_members': total_members,
            'newest_member': newest_member.get_full_name()  
        }
        return render(request,'formula/base.html', context=context_dict)
    
