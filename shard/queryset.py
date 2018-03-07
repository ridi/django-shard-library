# flake8: noqa: W0212 pylint: disable=protected-access
from django.db.models.query import QuerySet

__all__ = ('ShardQuerySet', )


class ShardQuerySet(QuerySet):
    def __init__(self, model, *args, **kwargs):
        super().__init__(model=model, *args, **kwargs)
        self._instance = None
        self._exact_lookups = {}

    def _clone(self):
        clone = super()._clone()
        clone._exact_lookups = self._exact_lookups.copy()
        return clone

    def _filter_or_exclude(self, negate, *args, **kwargs):
        clone = super()._filter_or_exclude(negate, *args, **kwargs)
        if getattr(clone, '_exact_lookups', None) is None:
            clone._exact_lookups = {}
        clone._exact_lookups.update(  # flake8: noqa: E1101 pylint: disable=no-member
            dict([(k, v) for k, v in kwargs.items() if '__' not in k])
        )
        return clone

    @property
    def db(self):
        if self._db:
            return self._db

        self._hints['exact_lookups'] = self._exact_lookups
        if not self._hints.get('instance') and getattr(self, '_instance', None):
            self._hints['instance'] = getattr(self, '_instance')

        return super().db

    def create(self, **kwargs):
        self._instance = self.model(**kwargs)
        return super().create(**kwargs)

    def get_or_create(self, defaults=None, **kwargs):
        defaults = defaults or {}
        lookup, _ = self._extract_model_params(defaults, **kwargs)
        self._exact_lookups = lookup
        return super(ShardQuerySet, self).get_or_create(defaults=defaults, **kwargs)

    def update_or_create(self, defaults=None, **kwargs):
        defaults = defaults or {}
        lookup, _ = self._extract_model_params(defaults, **kwargs)
        self._exact_lookups = lookup
        return super(ShardQuerySet, self).update_or_create(defaults=defaults, **kwargs)
