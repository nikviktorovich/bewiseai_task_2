import fastapi

import audio_converter.database.mappers
import audio_converter.apps.fastapi_app.routers.audio
import audio_converter.apps.fastapi_app.routers.users


def on_startup():
    audio_converter.database.mappers.start_mappers()


app = fastapi.FastAPI(on_startup=[on_startup])

# Routers
app.include_router(audio_converter.apps.fastapi_app.routers.audio.router)
app.include_router(audio_converter.apps.fastapi_app.routers.users.router)
