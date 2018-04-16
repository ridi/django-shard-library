from django.db.models.query import QuerySet

__all__ = ('ShardQuerySet', )


class ShardQuerySet(QuerySet):
    def __init__(self, model, *args, **kwargs):
        super().__init__(model=model, *args, **kwargs)
        self._instance = None

    @property
    def db(self):
        if self._db:
            return self._db

        if not self._hints.get('instance') and getattr(self, '_instance', None):
            self._hints['instance'] = getattr(self, '_instance')

        return super().db

    def create(self, **kwargs):
        self._instance = self.model(**kwargs)
        return super().create(**kwargs)
