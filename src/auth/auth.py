import os

from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)

bearer_transport = BearerTransport(tokenUrl="auth/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=os.getenv('SECRET_JWT', default='SECRET'),
        lifetime_seconds=os.getenv('AUTH_TOKEN_MAX_AGE', default=3600)
    )

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
