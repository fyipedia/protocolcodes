"""MCP server for protocolcodes."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from protocolcodes.api import ProtocolCodes

mcp = FastMCP("protocolcodes")


@mcp.tool()
def search_protocolcodes(query: str) -> dict[str, Any]:
    """Search protocolcodes.com for content matching the query."""
    with ProtocolCodes() as api:
        return api.search(query)
