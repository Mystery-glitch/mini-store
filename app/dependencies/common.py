from typing import Annotated

from fastapi import Header,Query

async def pagination(skip:Annotated[int,Query(ge=0)]=0,limit:Annotated[int,Query(ge=1,le=100)]=20):
    return {
        "skip":skip,
        "limit":limit
    }

async def get_requeste_language(accept_language:Annotated[str|None,Header()]=None):
    return accept_language or "en"