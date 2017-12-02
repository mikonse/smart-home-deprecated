import warnings
from importlib import import_module

import re
from django.apps import AppConfig
from django.conf import settings
from django.conf.urls import url, include

from . import urls


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        super().ready()

        if not hasattr(settings, 'INSTALLED_API_APPS'):
            warnings.warn("No api apps found in the global settings. "
                          "Are you sure you do not want an API?",
                          RuntimeWarning, stacklevel=2)

        for api_app in settings.INSTALLED_API_APPS:
            self.append_module_urls(api_app)

    @staticmethod
    def append_module_urls(module_name):
        # Try and import the base module
        try:
            module_urls = import_module(module_name + ".urls")
        except ImportError:
            raise RuntimeError("API module %s could not be imported" % module_name)

        # Get the routing regex for the app, defaults to the app name
        try:
            base_url = module_urls.url_regex
        except:
            base_url = r'^' + re.escape(module_name) + '/'

        urls.urlpatterns.append(url(base_url, include(module_urls.urlpatterns, namespace=module_name)))
