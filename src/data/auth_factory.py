from faker import Faker

from src.models.auth import LoginRequest, RegisterResponse, RegisterRequest

faker = Faker()


class RegisterFactory:
    @staticmethod
    def build(**overrides) -> RegisterRequest:
        data = {
            "email": faker.email(),
            "password": "123456",
            "role": "tester"
        }
        return RegisterRequest(**data)
