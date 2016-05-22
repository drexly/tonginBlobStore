from django import http
from django.template.response import TemplateResponse
from functools import update_wrapper
from django.utils.decorators import classonlymethod


class BaseView(object):
    """ Intentionally simple parent class for all views. Only implements
    dispatch-by-method and simple sanity checking.
    """
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']

    response_class = TemplateResponse

    def __init__(self, **kwargs):
        # Go through keyword arguments, and either save their values to our instance, or raise an error.
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    @classonlymethod
    def as_view(cls, **initkwargs):
        """ Main entry point for a request-response process.
        """
        # sanitize keyword arguments
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError(
                    u"%s() received a reserved method name %r." % (cls.__name__, key))
            if not hasattr(cls, key):
                raise TypeError(u"%s() received an invalid keyword %r" % (cls.__name__, key))

        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            return self.dispatch(request, *args, **kwargs)

        # take name and docstring from class
        update_wrapper(view, cls, updated=())

        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        self.request = request
        return handler(*args, **kwargs)

    def http_method_not_allowed(self, *args, **kwargs):
        allowed_methods = [m for m in self.http_method_names if hasattr(self, m)]
        return http.HttpResponseNotAllowed(allowed_methods)

    def render_to_response(self, template_name, context, **response_kwargs):
        """ Return a response with a template rendered with the given context.
        """
        context['request'] = self.request
        return self.response_class(
            request=self.request, template=template_name, context=context, **response_kwargs
        )
