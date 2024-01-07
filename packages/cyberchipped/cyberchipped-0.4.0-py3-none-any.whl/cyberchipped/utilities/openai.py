import asyncio
import os
from functools import lru_cache
from typing import Optional

from openai import AsyncClient


def get_client() -> AsyncClient:
    from cyberchipped import settings

    api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = (
            settings.openai.api_key.get_secret_value()
            if settings.openai.api_key
            else None
        )
    organization: Optional[str] = settings.openai.organization
    return _get_client_memoized(
        api_key=api_key, organization=organization, loop=asyncio.get_event_loop()
    )


@lru_cache
def _get_client_memoized(
    api_key: Optional[str],
    organization: Optional[str],
    loop: Optional[asyncio.AbstractEventLoop] = None,
) -> AsyncClient:
    """
    This function is memoized to ensure that only one instance of the client is
    created for a given api key / organization / loop tuple.

    The `loop` is an important key to ensure that the client is not re-used
    across multiple event loops (which can happen when using the `run_sync`
    function). Attempting to re-use the client across multiple event loops
    can result in a `RuntimeError: Event loop is closed` error or infinite hangs.
    """
    return AsyncClient(
        api_key=api_key,
        organization=organization,
    )
