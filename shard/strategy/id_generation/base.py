
__all__ = ('BaseIDGenerationStrategy', )


class BaseIDGenerationStrategy:
    def get_next_id(self, instance):
        raise NotImplementedError
