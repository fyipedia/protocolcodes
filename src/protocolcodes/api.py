"""HTTP API client for protocolcodes.com REST endpoints.

Requires the ``api`` extra: ``pip install protocolcodes[api]``

Usage::

    from protocolcodes.api import ProtocolCodes

    with ProtocolCodes() as api:
        results = api.search("404")
        print(results)
"""

from __future__ import annotations

from typing import Any

import httpx


class ProtocolCodes:
    """API client for the protocolcodes.com REST API.

    Args:
        base_url: API base URL. Defaults to ``https://protocolcodes.com``.
        timeout: Request timeout in seconds. Defaults to ``10.0``.
    """

    def __init__(
        self,
        base_url: str = "https://protocolcodes.com",
        timeout: float = 10.0,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(path, params={k: v for k, v in params.items() if v is not None})
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    def search(self, query: str) -> dict[str, Any]:
        """Search across all content.

        Args:
            query: Search term (e.g. ``"404"``).
        """
        return self._get("/api/search/", q=query)

    def close(self) -> None:
        """Close the underlying HTTP connection."""
        self._client.close()

    def __enter__(self) -> ProtocolCodes:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
