from django.urls import reverse, NoReverseMatch
from django.utils.deprecation import MiddlewareMixin

fields_to_omit = ['create_post', 'create_topic']
class BreadcrumbMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info.lstrip('/').split('/')
        breadcrumbs = []
        url = '/'
        for slug in path:
            if not slug:
                continue
            if slug == "accounts":
                slug = "formula"
            if slug in fields_to_omit:
                continue
            url += slug + '/'
            if slug =='profile':
                continue
            slug = slug.capitalize()
            try:
                breadcrumbs.append((reverse(url), slug))
            except NoReverseMatch:
                breadcrumbs.append((url, slug))
        request.breadcrumbs = breadcrumbs
