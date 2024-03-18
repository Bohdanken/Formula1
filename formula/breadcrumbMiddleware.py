from django.urls import reverse, NoReverseMatch
from django.utils.deprecation import MiddlewareMixin

class BreadcrumbMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info.lstrip('/').split('/')
        breadcrumbs = [('/', 'Home')]
        url = '/'
        for slug in path:
            if not slug:
                continue
            url += slug + '/'
            try:
                breadcrumbs.append((reverse(url), slug))
            except NoReverseMatch:
                breadcrumbs.append((url, slug))
        print(breadcrumbs)
        request.breadcrumbs = breadcrumbs
