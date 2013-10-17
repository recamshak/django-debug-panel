from django.core.cache import get_cache
from django.core.cache.backends.base import InvalidCacheBackendError

try:
    cache = get_cache('debug-panel')
except InvalidCacheBackendError:
    from django.core.cache import cache