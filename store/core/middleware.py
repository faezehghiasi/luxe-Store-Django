from django.utils import translation
from django.conf import settings

class CustomLocaleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get language from session
        language = request.session.get('django_language')
        if language and language in [lang[0] for lang in settings.LANGUAGES]:
            translation.activate(language)
            request.LANGUAGE_CODE = language
        else:
            # Use default language
            translation.activate(settings.LANGUAGE_CODE)
            request.LANGUAGE_CODE = settings.LANGUAGE_CODE
        
        response = self.get_response(request)
        return response 