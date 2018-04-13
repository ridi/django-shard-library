
# Django-Shard-Library
[![Build Status](https://travis-ci.org/ridi/django-shard-library.svg?branch=master)](https://travis-ci.org/ridi/django-shard-library)

## Introduction
- 장고 ORM에서 샤드기능을 지원하기 위한 라이브러리 입니다.

## Requirement
- `Django 2.0.0` or higher
- `Python 3.6` or higher
- `MySQL` or `Mariadb` only

## Usage
#### Setup
``` python
DATABASES = ConfigHelper.database_configs(
    unshard = {
        'default': {
            'master': 'mysql://user:pwd@host/metadata',
            'slaves': ['mysql://user:pwd@host/metadata?sql_mode=STRICT_TRANS_TABLE&charset=utf8', ]
        },
    },
    shard = {
        'SHARD_NAME': {
            'shard_options': {
                'database_name': 'product',
                'logical_count': 4,
            },
            'db_options': {  # Optional
                'sql_mode': 'STRICT_TRANS_TABLE',
                'charset': 'utf8',
            },
            'shards': [
                {
                    'master': 'mysql://user:pwd@host/',
                    'slaves': ['mysql://user:pwd@host/', 'mysql://user:pwd@host/',]
                },
                {
                    'master': 'mysql://user:pwd@host/',
                    'slaves': ['mysql://user:pwd@host/', 'mysql://user:pwd@host/',]
                }
            ],
        },
    },
)

```

#### Model
``` python
class ShardModel(ShardMixin, models.Model):
    user_id = models.IntegerField(null=False, verbose_name='User Idx')

    shard_group = 'SHARD_NAME'
    shard_key_name = 'user_id'
```

- `shard_key` is supported only integer type.

## Snippets
We don't want to having dependency of celery and redis.  
If you want to using `shard_static`, you refer to this

#### Supervisor for running syncer
``` python
@task  # celery
def wrap_sync_static(model_name, database_alias):
    sync_static_service.sync_static(model_name, database_alias)

def run_sync_supervisor():
    static_models = [
        ShardStaticA,
        ShardStaticAll,
        # ...
    ]

    for static_model in static_models:
        databases = get_master_databases_for_shard() \
            if static_model.shard_group == ALL_SHARD_GROUP else \
            get_master_databases_by_shard_group(static_model.shard_group)

        for database in databases:
            wrap_sync_static.delay(static_model._meta.label, database)
```

#### RedisLockManager
``` python

class RedisLockManager(BaseLockManager):
    def get_connection():
        return Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DATABASE)

    def is_locked(self) -> bool:
        conn = self.get_connection()
        value = conn.get(self.key)
        return value is not None

    def lock(self) -> bool:
        conn = self.get_connection()
        return conn.set(self.key, self.uuid, ex=self.ttl, nx=True)

    def ping(self) -> bool:
        conn = self.get_connection()
        return conn.expire(self.key, self.ttl)

    def release(self) -> bool:
        conn = self.get_connection()
        return conn.delete(self.key)
```

## Dependency
- [dj-database-url](https://github.com/kennethreitz/dj-database-url)

## TODO
- Feature automatically find static models (python meta programming or different way)
- Write example app
- Write docs

## Prior art
- https://github.com/JBKahn/django-sharding
