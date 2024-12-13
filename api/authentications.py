from django.core.cache import cache
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from core.django_conf.settings import CACHE_TIMEOUT


class CachedTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization')

        if not auth or not auth.startswith('Token '):
            return None

        token = auth.split(' ')[1]
        cached_user = cache.get(f'token_{token}')

        if cached_user:
            return cached_user, token

        user, token = super().authenticate(request)

        if user is None:
            raise AuthenticationFailed('Неверный токен')

        cache.set(f'token_{token}', user, timeout=CACHE_TIMEOUT)
        return user, token
