from winter.authentication import (
    AuthenticationMiddleware, AuthenticationBackend
)


class AuthMixin:

    def spring_auth(self):
        self.app.add_middleware(
            AuthenticationMiddleware,
            backend=AuthenticationBackend()
        )
