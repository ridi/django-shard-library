
# Django-Shard-Library
[![Build Status](https://travis-ci.org/ridi/django-shard-library.svg?branch=master)](https://travis-ci.org/ridi/django-shard-library)

## Introduction
- Python library for supporting sharding in Django ORM.

## Requirement
- `Django 2.0.0` or higher
- `Python 3.6` or higher
- `MySQL` or `Mariadb` only

## Dependency
- [dj-database-url](https://github.com/kennethreitz/dj-database-url)

## Usage
#### If you want to use only shard
``` python
# in settings.py

INSTALLED_APPS = [
    # ...
    'shard',
]

DATABASES = ConfigHelper.generate_database_configs(
    unshard = {
        'default': {
            'conn_max_age': 0,
            'master': {
                'url': 'mysql://user:pwd@host/metadata',
                'conn_max_age': 1000,  # Optional
            },
            'slaves': [{
                'url': 'mysql://user:pwd@host/metadata?sql_mode=STRICT_TRANS_TABLE&charset=utf8',
                'conn_max_age': 500,  # Optional
            }]
        },
    },
    shard = {
        'SHARD_GROUP_A': {
            'database_name': 'product',
            'logical_count': 4,
            'conn_max_age': 0,  # Optional
            'options': {  # Optional
                'sql_mode': 'STRICT_TRANS_TABLE',
                'charset': 'utf8',
            },
            'shards': [
                {
                    'master': {
                        'url': 'mysql://user:pwd@host/',
                        'conn_max_age: 400,  # Optional
                        'options': {  # Optional
                            'charset': 'latin',
                        },
                    },
                    'slaves': [{
                        'url': 'mysql://user:pwd@host/',
                        'conn_max_age: 600,  # Optional
                    }, {
                        'url': 'mysql://user:pwd@host/',
                        'options': {  # Optional
                            'charset': 'latin',
                        },
                    },]
                },
                {
                    'master': { 'url': 'mysql://user:pwd@host/', },
                    'slaves': [{ 'url': 'mysql://user:pwd@host/' }, { 'url': 'mysql://user:pwd@host/' },]
                },
            ],
        },
    },
)
DATABASE_ROUTERS = ['shard.routers.specific.SpecificRouter', 'shard.routers.shard.ShardRouter']
```
``` python
# in models.py
class ShardModel(ShardMixin, models.Model):
    user_id = models.IntegerField(null=False, verbose_name='User Idx')

    shard_group = 'SHARD_GROUP_A'
    shard_key_name = 'user_id'
```
- `shard_key` is supported only integer type.

#### If you want to use shard_static together.
``` python
# in settings.py

INSTALLED_APPS = [
    # ...
    'shard',
    'shard_static',
]

DATABASES = ConfigHelper.generate_database_configs(
    # ...
)

DATABASE_ROUTERS = ['shard.routers.specific.SpecificRouter', 'shard_static.routers.ShardStaticRouter']
```
``` python
# in models.py
class ExampleStaticModel(BaseShardStaticModel):
    field1 = models.CharField(max_length=64, null=False)
    field2 = models.CharField(max_length=64, null=False)
```

- Must includes `shard_static` to `INSTALLED_APPS`
- Must implement `transmitter` and `BaseStaticTransmitStatus`.
- Must use `shard_static.routers.ShardStaticRouter`
    - `ShardStaticRouter` is extended feature that all of the `ShardRouter`.

#### If you want to change replica count
```python
# in settings.py

SHARD_REPLICA_COUNT_SETTING = {
    'SHARD_GROUP_A': 1024,
    'SHARD_GROUP_B': 128,
}
```

- Default is 512.

## How to run test
- Step 1: Run database for testing.  
`make run-test-db`

- Step 2: Run test.  
`make test`

- Step 3: When end of test, you stop to database.  
`make stop-test-db`

## Warning
- If you want to use this with django 2.1.0, Be careful missing shard key when getting queryset by raw query.

## Prior art
- https://github.com/JBKahn/django-sharding