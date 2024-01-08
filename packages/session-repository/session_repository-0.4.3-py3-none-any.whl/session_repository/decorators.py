# SQLALCHEMY
from sqlalchemy.orm import Session


def with_session(
    param_session: str = "session",
):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if not isinstance(self, (SessionRepository, SessionService)):
                raise TypeError(
                    f"{param_session} must be instance of {SessionRepository.__name__} or {SessionService.__name__}"
                )

            session = kwargs.get(param_session)

            if session is None:
                with self.session_manager() as session:
                    kwargs[param_session] = session
            elif not isinstance(session, Session):
                raise TypeError(
                    f"{param_session} must be instance of {Session.__name__}"
                )

            return func(self, *args, **kwargs)

        return wrapper

    return decorator


from session_repository.models.repository import SessionRepository
from session_repository.models.service import SessionService
