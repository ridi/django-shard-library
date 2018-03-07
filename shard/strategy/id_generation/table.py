from django.apps import apps
from django.db import connections, transaction
from django.utils.deconstruct import deconstructible

from shard.models import TableStrategyModel
from shard.strategy.id_generation.base import BaseIDGenerationStrategy

__all__ = ('TableStrategy', )


@deconstructible
class TableStrategy(BaseIDGenerationStrategy):
    def __init__(self, source_model):
        self.source_model = source_model

    def get_next_id(self, instance):
        model = self._get_model()

        if not issubclass(model, TableStrategyModel):
            raise ValueError('ID발급에 사용할 수 없는 모델입니다.')

        model_db = getattr(model, '_specific_database', 'default')
        with transaction.atomic(model_db):
            cursor = connections[model_db].cursor()

            sql = 'INSERT INTO %s DEFAULT VALUES' % (
                model._meta.db_table,  # flake8: noqa: W0212  # pylint: disable=protected-access
            )

            cursor.execute(sql)

        return cursor.cursor.lastrowid

    def _get_model(self):
        splited = self.source_model.split('.')

        app_label = splited[0]
        app = apps.get_app_config(app_label)
        return app.get_model(splited[-1])
