from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import util

AVAILABLE_LANGUAGES = ["en", "ru"]


class LanguageMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        lang = request.query_params.get("lang")

        if lang not in AVAILABLE_LANGUAGES:
            lang = "ru"

        common = util.load_lang_file(lang, "common.json")
        url = request.url.path

        translation = common.get(url.replace("/", ""))
        name = common.get('name')
        request.state.page_title = f"{translation} / {name}" if translation else name
        request.state.common_translations = common

        request.state.lang = lang
        response = await call_next(request)
        return response
