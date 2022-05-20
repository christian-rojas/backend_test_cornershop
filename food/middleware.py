from django.http import HttpResponseRedirect


class noraMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.path.startswith("/food")
            or request.path.startswith("/nora/admin")
        ) and not request.user.is_superuser:
            print(request.user.is_superuser)
            return HttpResponseRedirect("/home")
        return self.get_response(request)
