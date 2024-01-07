
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware


from spacestar import spacestar_settings


session_middleware = Middleware(SessionMiddleware, secret_key=spacestar_settings.session_secret)