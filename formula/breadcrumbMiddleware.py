

class BreadcrumbMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info.lstrip('/').split('/')
        breadcrumbs = ['Home']
        url = '/'
        for slug in path:
            if not slug:
                continue
            url += slug + '/'
            try:
                breadcrumbs.append((reverse(url), slug))
            except NoReverseMatch:
                breadcrumbs.append((url, slug))
        request.breadcrumbs = breadcrumbs
