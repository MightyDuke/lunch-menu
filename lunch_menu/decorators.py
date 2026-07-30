from fastapi import Depends, Response

def add_private_cache_header(response: Response):
    response.headers["Cache-control"] = "private, must-revalidate"