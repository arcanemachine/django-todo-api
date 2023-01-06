# from django.conf import settings


def debug_middleware(get_response):
    """Add custom logic to any view."""

    def middleware(request):
        response = get_response(request)

        try:
            from todo.middleware.do_not_commit_to_repo import code_block

            code_block(request, response)
        except ImportError:
            pass

        return response

    return middleware
