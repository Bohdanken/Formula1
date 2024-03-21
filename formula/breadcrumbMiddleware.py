from django.urls import reverse, NoReverseMatch
from django.utils.deprecation import MiddlewareMixin

class BreadcrumbMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info.lstrip('/').split('/')
        breadcrumbs = []
        url = '/'
        for slug in path:
            if not slug:
                continue
            if slug=="accounts":
                slug="formula"
            url += slug + '/'
            slug=slug.capitalize()
            try:
                breadcrumbs.append((reverse(url), slug))
            except NoReverseMatch:
                breadcrumbs.append((url, slug))
        print(breadcrumbs)
        request.breadcrumbs = breadcrumbs
