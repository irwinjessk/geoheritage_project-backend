"""
Middleware personnalisé pour GeoHeritage
Exemption CSRF pour les endpoints API
"""

from django.middleware.csrf import CsrfViewMiddleware
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import re


class DisableCSRFForAPI(MiddlewareMixin):
    """
    Middleware pour désactiver CSRF pour les endpoints API
    """
    def process_request(self, request):
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
