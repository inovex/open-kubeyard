import os

MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY', '')
CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': '{{ tuple (default "helm-redis" .Values.redis.name) . | include "fqdn" }}',
    'CACHE_REDIS_PORT': {{ default "6379" .Values.redis.port }},
    'CACHE_REDIS_DB': 1,
    'CACHE_REDIS_URL': 'redis://{{ tuple (default "helm-redis" .Values.redis.name) }}:{{ default "6379" .Values.redis.port }}/1'}
SQLALCHEMY_DATABASE_URI = 'mysql://superset:superset@{{ default "mysql-service" .Values.mysql.name }}:{{ default "3306" .Values.mysql.port }}/superset'
SECRET_KEY = '{{ randAlphaNum 24 | b64enc }}'
