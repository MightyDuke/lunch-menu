from typing import Annotated
from secrets import token_urlsafe
from urllib.parse import urlencode
from textwrap import dedent
from fastapi import APIRouter, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter()
router.frontend("/", directory = f"web/src/", fallback = None)

@router.get("/auth", response_class = RedirectResponse)
async def auth(
    url: Annotated[str, Query()],
    client_id: Annotated[str, Query()],
    redirect_uri: Annotated[str, Query()]
):
    parameters = {
        "client_id": client_id,
        "response_type": "id_token", 
        "scope": "openid profile",
        "redirect_uri": f"{redirect_uri}/auth",
        "prompt": "select_account",
        "response_mode": "form_post",
        "nonce": token_urlsafe(16)
    } 

    return f"{url}?{urlencode(parameters)}"

@router.post("/auth", response_class = HTMLResponse)
async def auth_post(
    id_token: Annotated[str | None, Form()] = None,
):
    return dedent(f"""
        <!DOCTYPE html>
        <html lang="cs">
        <meta name="color-scheme" content="light dark">
        <title>Přihlášení</title>
        <script>
            try {{ 
                window.opener.sendSessionToken({f"\"{id_token}\"" if id_token is not None else "null"}); 
            }} finally {{ 
                window.close(); 
            }} 
        </script>
    """)