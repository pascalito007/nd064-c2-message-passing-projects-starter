from .models import Person  # noqa
from .schemas import PersonSchema  # noqa


def register_routes(api, app, root="api"):
    from .controllers import api as udaconnect_api

    api.add_namespace(udaconnect_api, path=f"/{root}")
