from django.db import transaction
from core.services import BaseService
from .models import AdminProfile
from users.services import UserService

class AdminService(BaseService):
    model = AdminProfile

    @classmethod
    @transaction.atomic
    def create_admin(cls, user_data, admin_data):
        # 1. Create User via UserService
        user = UserService.create_user(
            password=user_data.get('password'),
            email=user_data.get('email'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            role='ADMIN'
        )
        # 2. Create Admin Profile
        admin_profile = cls.create(user=user, **admin_data)
        return admin_profile

    @classmethod
    @transaction.atomic
    def update_admin(cls, admin_id, user_data=None, admin_data=None):
        admin_profile = cls.get_by_id(admin_id)
        if user_data:
            user = admin_profile.user
            for field, value in user_data.items():
                setattr(user, field, value)
            user.save()
        if admin_data:
            for field, value in admin_data.items():
                setattr(admin_profile, field, value)
            admin_profile.save()
        return admin_profile

    @classmethod
    @transaction.atomic
    def delete_admin(cls, admin_id):
        admin_profile = cls.get_by_id(admin_id)
        user = admin_profile.user
        admin_profile.delete()
        user.delete()
        return True
