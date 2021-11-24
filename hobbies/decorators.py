from django.http import HttpResponseForbidden


def user_login_required():
    """
    Decorator for api that checks user is logged in
    and authenticated, if not, it returns a Forbidden
    response
    """

    def decorator(api_func):
        def _wrapped_api_function(request, *args, **kwargs):
            if (request.user.is_authenticated):
                return api_func(request, *args, **kwargs)
            return HttpResponseForbidden("Not logged in")
        return _wrapped_api_function
    return decorator
