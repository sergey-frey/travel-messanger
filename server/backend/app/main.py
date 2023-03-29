from backend.api import api_router
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.db import settings
from backend.utils.exception_handlers import database_error_handler, database_not_found_handler, http_exception_handler
from sqlalchemy.exc import DBAPIError, NoResultFound
from backend.db import database
from fastapi.staticfiles import StaticFiles


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        terms_of_service="http://www.fastapi.org",
        contact=dict(
            name="Telegram",
            url="https://www.telegram.org/@Holucrap",
            email="maijor18@mail.ru",
        ),
        license_info=dict(
            name="Apache 2.0",
            url="https://www.apache.org/licenses/LICENSE-2.0.html"
        ),
        openapi_url="{0}/openapi.json".format(settings.DOCS),
        swagger_ui_parameters=settings.SWAGGER_UI_PARAMETERS,
    )

    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin)
                           for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    # app.mount('/client/src/assets/', StaticFiles(directory='/client/src/assets/'), name='assets')
    app.include_router(api_router, prefix=settings.API)
    app.dependency_overrides.setdefault(*database.override_session)
    app.add_exception_handler(DBAPIError, database_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(NoResultFound, database_not_found_handler)

    return app
