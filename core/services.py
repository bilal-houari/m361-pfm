from django.db import transaction

class BaseService:
    model = None

    @classmethod
    def list(cls):
        return cls.model.objects.all()

    @classmethod
    def get_by_id(cls, obj_id):
        return cls.model.objects.get(id=obj_id)

    @classmethod
    def create(cls, **kwargs):
        return cls.model.objects.create(**kwargs)

    @classmethod
    def update(cls, obj_id, **kwargs):
        obj = cls.get_by_id(obj_id)
        for field, value in kwargs.items():
            setattr(obj, field, value)
        obj.save()
        return obj

    @classmethod
    def delete(cls, obj_id):
        obj = cls.get_by_id(obj_id)
        obj.delete()
        return True
