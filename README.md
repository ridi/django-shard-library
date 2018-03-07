
# Django-Shard-Library

## Introduction

## Dependency
- [dj-database-url](https://github.com/kennethreitz/dj-database-url)

## Usage
### Setup
``` python
# shard = instance
# logical_shard = database
# replica = code상 shard_count

DATABASES = generate_databases(
    unshard = {
        'default': {
            'master': 'mysql://user:pwd@host/metadata',
            'slaves': ['mysql://user:pwd@host/metadata', ]
        },
    },
    shard = {
        'SHARD_NAME': {
            'options': {
                'database_name': 'product',
                'logical_count': 4,
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

SHARD_REPLICA_COUNT_SETTING = {
    'SHARD_NAME': 1024, # default: 1024
}

```

### Model
``` python
class ShardModel(ShardMixin, models.Model):
    user_id = models.IntegerField(null=False, verbose_name='User Idx')

    shard_group = 'SHARD_NAME'
    shard_key_name = 'user_id'
```

- Shard Key는 현재 Integer만 지원합니다.

## TODO

- 모든 샤드에 공유되는 Static데이터기능 구현
    - 하나의 모델로 동작해야함
- migration
