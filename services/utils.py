from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response

from core.django_conf.settings import CACHE_TIMEOUT


def response_action_method(request, instance, *args, **kwargs):
    """
    Возвращает response наследованный от класса для списка и объекта.
    """
    class_calc = (type(instance), instance)
    if instance.action == 'list':
        return super(*class_calc).list(request, *args, **kwargs)
    return super(*class_calc).retrieve(request, *args, **kwargs)


def check_response_cache(instance, request, cache_key, *args, **kwargs):
    cached_object = cache.get(cache_key)
    if cached_object is not None:
        return Response(cached_object, status=status.HTTP_200_OK)
    response = response_action_method(request, instance, *args, **kwargs)
    cache.set(cache_key, response.data, timeout=CACHE_TIMEOUT)
    return response


def delete_wallet_cache(instance_id, user_id):
    """Удаляет кэш после создания, обновления и удаления счета"""
    cache.delete(f'wallet_list_{user_id}')
    cache.delete(f'wallet_{instance_id}')
