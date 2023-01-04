# from django.conf import settings


def debug_middleware(get_response):
    """Easily insert a breakpoint into any called view."""

    def middleware(request):
        response = get_response(request)

        # if settings.DEBUG and request.GET.get("debug"):
        #     breakpoint()
        breakpoint()

        return response

    return middleware
