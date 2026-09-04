from typing import Annotated
from pathlib import Path
from textwrap import dedent
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse

router = APIRouter(include_in_schema = False)

router.frontend(
    "/", 
    directory = "web/dist/" if Path("web/dist/").exists() else "web/src/", 
    fallback = "404.html"
)

@router.post("/auth", response_class = HTMLResponse)
async def auth_post(
    id_token: Annotated[str | None, Form()] = None
):
    return dedent(f"""
        <!DOCTYPE html>
        <html lang="cs">
        <meta name="color-scheme" content="light dark">
        <title>Přihlášení</title>
        <script>
            try {{ 
                window.opener.sendIdToken({f"\"{id_token}\"" if id_token is not None else "null"}); 
            }} finally {{ 
                window.close(); 
            }} 
        </script>
    """)