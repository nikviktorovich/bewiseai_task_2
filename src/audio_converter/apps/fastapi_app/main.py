import fastapi
import fastapi.responses
from fastapi import status

import audio_converter.common.errors
import audio_converter.database.mappers
import audio_converter.apps.fastapi_app.routers.audio
import audio_converter.apps.fastapi_app.routers.users


def on_startup():
    audio_converter.database.mappers.start_mappers()


app = fastapi.FastAPI(on_startup=[on_startup])


# Exception handlers
@app.exception_handler(audio_converter.common.errors.AudioError)
def handle_audio_error(
    request: fastapi.Request,
    exception: audio_converter.common.errors.AudioError,
):
    return fastapi.responses.JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'detail': str(exception),
        },
    )


@app.exception_handler(audio_converter.common.errors.AuthError)
def handle_auth_error(
    request: fastapi.Request,
    exception: audio_converter.common.errors.AuthError,
):
    return fastapi.responses.JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            'detail': str(exception),
        },
    )


@app.exception_handler(audio_converter.common.errors.EntityNotFoundError)
def handle_entity_not_found_error(
    request: fastapi.Request,
    exception: audio_converter.common.errors.EntityNotFoundError,
):
    return fastapi.responses.JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            'detail': str(exception),
        },
    )


@app.exception_handler(audio_converter.common.errors.EntityAlreadyExists)
def handle_entity_already_exists_error(
    request: fastapi.Request,
    exception: audio_converter.common.errors.EntityAlreadyExists,
):
    return fastapi.responses.JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'detail': str(exception),
        },
    )


@app.exception_handler(FileNotFoundError)
def handle_file_not_found_error(
    request: fastapi.Request,
    exception: FileNotFoundError,
):
    return fastapi.responses.JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            'detail': str(exception),
        },
    )


@app.exception_handler(audio_converter.common.errors.BadUUIDError)
def handle_bad_uuid_error(
    request: fastapi.Request,
    exception: FileNotFoundError,
):
    return fastapi.responses.JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            'detail': str(exception),
        },
    )


# Routers
app.include_router(audio_converter.apps.fastapi_app.routers.audio.router)
app.include_router(audio_converter.apps.fastapi_app.routers.users.router)
