from django.contrib.auth import get_user_model
from core.services import BaseService

User = get_user_model()

class UserService(BaseService):
    model = User

    @classmethod
    def create_user(cls, password, email, first_name, last_name, role, username=None):
        if not username:
            username = email
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        return user
