"""Command-line interface for protocolcodes."""

from __future__ import annotations

import json

import typer

from protocolcodes.api import ProtocolCodes

app = typer.Typer(help="ProtocolCodes — HTTP status codes and protocol reference API client.")


@app.command()
def search(query: str) -> None:
    """Search protocolcodes.com."""
    with ProtocolCodes() as api:
        result = api.search(query)
        typer.echo(json.dumps(result, indent=2))
