import factory
from factory.django import DjangoModelFactory

from challenge.core.models import User


class UserAdminFactory(DjangoModelFactory):
    email = factory.Faker("email")
    full_name = factory.Faker("user_name")
    password = factory.PostGenerationMethodCall('set_password', 'password')
    is_staff = True
    is_superuser = True

    class Meta:
        model = User
        
        
class UserCandidateFactory(DjangoModelFactory):
    email = factory.Faker("email")
    full_name = factory.Faker("user_name")
    password = factory.PostGenerationMethodCall('set_password', 'password')

    class Meta:
        model = User


class UserEmployeeFactory(DjangoModelFactory):
    email = factory.Faker("email")
    full_name = factory.Faker("user_name")
    password = factory.PostGenerationMethodCall('set_password', 'password')

    class Meta:
        model = User
