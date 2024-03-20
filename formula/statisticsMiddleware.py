
from django.utils.deprecation import MiddlewareMixin
from formula.models import Post, Topic, CustomUser

class StatisticsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        
        total_posts = Post.objects.all().count()
        total_topics = Topic.objects.all().count()
        #total_members = CustomUser.objects.count()
        #newest_member = CustomUser.objects.latest('date_joined')
        # Attach the statistics to the request object
        request.total_posts = total_posts
        request.total_topics = total_topics
        #request.total_members = total_members
        #request.newest_member = newest_member

        
    


    