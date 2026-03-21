# protocolcodes

[![PyPI version](https://agentgif.com/badge/pypi/protocolcodes/version.svg)](https://pypi.org/project/protocolcodes/)
[![Python](https://img.shields.io/pypi/pyversions/protocolcodes)](https://pypi.org/project/protocolcodes/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)](https://pypi.org/project/protocolcodes/)

Python API client for HTTP status codes and protocol references. Look up status codes with RFC citations, explore response code categories (1xx-5xx), query header field definitions, and retrieve REST API semantics — all from [StatusCodeFYI](https://statuscodefyi.com/), a protocol reference platform for web developers and API designers.

StatusCodeFYI catalogs every registered HTTP status code with its RFC source, category, typical use case, server behavior, and client handling — providing structured access to the HTTP specification used by API developers, DevOps engineers, and web framework authors.

> **Look up HTTP status codes at [statuscodefyi.com](https://statuscodefyi.com/)** — browse by [category](https://statuscodefyi.com/categories/), search [status codes](https://statuscodefyi.com/status-codes/), and view RFC details.

<p align="center">
  <img src="https://raw.githubusercontent.com/fyipedia/protocolcodes/main/demo.gif" alt="protocolcodes demo — HTTP status code lookup, RFC references, and REST semantics in Python" width="800">
</p>

## Table of Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [What You Can Do](#what-you-can-do)
  - [HTTP Status Code Classes](#http-status-code-classes)
  - [REST API Semantics](#rest-api-semantics)
  - [Common Status Codes in Practice](#common-status-codes-in-practice)
  - [RFC Standards and Extensions](#rfc-standards-and-extensions)
- [Command-Line Interface](#command-line-interface)
- [MCP Server (Claude, Cursor, Windsurf)](#mcp-server-claude-cursor-windsurf)
- [REST API Client](#rest-api-client)
- [API Reference](#api-reference)
- [Learn More About HTTP](#learn-more-about-http)
- [Also Available](#also-available)
- [Network FYI Family](#network-fyi-family)
- [License](#license)

## Install

```bash
pip install protocolcodes                # Core (zero deps)
pip install "protocolcodes[cli]"         # + Command-line interface
pip install "protocolcodes[mcp]"         # + MCP server for AI assistants
pip install "protocolcodes[api]"         # + HTTP client for statuscodefyi.com API
pip install "protocolcodes[all]"         # Everything
```

## Quick Start

```python
from protocolcodes.api import ProtocolCodes

with ProtocolCodes() as api:
    # Look up a status code
    code = api.get_status_code(404)
    print(code["code"])            # 404
    print(code["phrase"])          # Not Found
    print(code["category"])        # Client Error (4xx)
    print(code["rfc"])             # RFC 9110

    # List codes by category
    client_errors = api.list_status_codes(category="4xx")
    for c in client_errors:
        print(f"{c['code']} {c['phrase']}")

    # Search status codes
    results = api.search("redirect")
```

## What You Can Do

### HTTP Status Code Classes

HTTP response status codes are divided into five classes by their first digit. Each class indicates a general category of response — from informational acknowledgments (1xx) through successful operations (2xx), redirections (3xx), client errors (4xx), to server failures (5xx).

| Class | Range | Meaning | Common Codes |
|-------|-------|---------|-------------|
| 1xx Informational | 100-199 | Request received, continuing | 100 Continue, 101 Switching Protocols |
| 2xx Success | 200-299 | Request successfully processed | 200 OK, 201 Created, 204 No Content |
| 3xx Redirection | 300-399 | Further action needed | 301 Moved Permanently, 304 Not Modified |
| 4xx Client Error | 400-499 | Client sent bad request | 400 Bad Request, 401 Unauthorized, 404 Not Found |
| 5xx Server Error | 500-599 | Server failed to process | 500 Internal Server Error, 502 Bad Gateway |

```python
from protocolcodes.api import ProtocolCodes

with ProtocolCodes() as api:
    # Browse status code categories
    categories = api.list_categories()
    for cat in categories:
        print(f"{cat['name']}: {cat['count']} status codes")

    # Get all codes in a category
    success = api.list_status_codes(category="2xx")
    for code in success:
        print(f"{code['code']} {code['phrase']}")
```

Learn more: [Status Code Categories](https://statuscodefyi.com/categories/) · [Glossary](https://statuscodefyi.com/glossary/)

### REST API Semantics

RESTful APIs map HTTP methods to CRUD operations, and status codes communicate the outcome. Proper status code usage is a hallmark of well-designed APIs — returning 201 for resource creation, 204 for successful deletion, and 409 for conflict resolution.

| Method | Operation | Success Code | Error Codes |
|--------|----------|-------------|-------------|
| GET | Read | 200 OK | 404 Not Found |
| POST | Create | 201 Created | 400 Bad Request, 409 Conflict |
| PUT | Replace | 200 OK / 204 No Content | 404 Not Found |
| PATCH | Partial Update | 200 OK | 422 Unprocessable Entity |
| DELETE | Remove | 204 No Content | 404 Not Found |

```python
from protocolcodes.api import ProtocolCodes

with ProtocolCodes() as api:
    # Look up the correct status code for an API response
    created = api.get_status_code(201)
    print(f"{created['code']} {created['phrase']}")
    print(f"Use case: {created.get('description')}")
    # 201 Created — returned when a new resource is successfully created
```

Learn more: [REST Semantics](https://statuscodefyi.com/guides/) · [Glossary](https://statuscodefyi.com/glossary/)

### Common Status Codes in Practice

While the HTTP specification defines over 60 status codes, a smaller set dominates real-world usage. Understanding the distinction between similar codes (301 vs 302, 401 vs 403, 502 vs 504) is essential for debugging and API design.

| Code | Phrase | When to Use |
|------|--------|------------|
| 200 | OK | Standard successful response |
| 201 | Created | Resource created (POST) |
| 204 | No Content | Success with no body (DELETE) |
| 301 | Moved Permanently | Permanent URL change (SEO) |
| 302 | Found | Temporary redirect |
| 304 | Not Modified | Cache validation (ETag/If-Modified-Since) |
| 400 | Bad Request | Malformed syntax, invalid params |
| 401 | Unauthorized | Missing/invalid authentication |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource does not exist |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unhandled server exception |
| 502 | Bad Gateway | Upstream server error (proxy) |
| 503 | Service Unavailable | Server overloaded or in maintenance |

```python
from protocolcodes.api import ProtocolCodes

with ProtocolCodes() as api:
    # Compare similar status codes
    code_401 = api.get_status_code(401)
    code_403 = api.get_status_code(403)
    print(f"401: {code_401['phrase']} — {code_401.get('description')}")
    print(f"403: {code_403['phrase']} — {code_403.get('description')}")
```

Learn more: [Status Codes](https://statuscodefyi.com/status-codes/) · [Guides](https://statuscodefyi.com/guides/)

### RFC Standards and Extensions

HTTP status codes are defined across multiple RFCs. The core specification is RFC 9110 (HTTP Semantics), while extensions add codes for specific purposes — 418 (RFC 2324, April Fools'), 429 (RFC 6585, rate limiting), and 451 (RFC 7725, legal censorship, a reference to Fahrenheit 451).

| RFC | Status Codes | Topic |
|-----|-------------|-------|
| RFC 9110 | Core 1xx-5xx | HTTP Semantics (2022) |
| RFC 6585 | 428, 429, 431, 511 | Additional codes (rate limiting, etc.) |
| RFC 7725 | 451 | Unavailable for Legal Reasons |
| RFC 8297 | 103 | Early Hints |
| RFC 2324 | 418 | I'm a Teapot (HTCPCP) |

```python
from protocolcodes.api import ProtocolCodes

with ProtocolCodes() as api:
    # Look up RFC reference for a status code
    code = api.get_status_code(429)
    print(f"{code['code']} {code['phrase']}")
    print(f"RFC: {code.get('rfc')}")       # RFC 6585
    print(f"Section: {code.get('rfc_section')}")
```

Learn more: [RFC References](https://statuscodefyi.com/guides/) · [API Documentation](https://statuscodefyi.com/developers/)

## Command-Line Interface

```bash
pip install "protocolcodes[cli]"

protocolcodes status 404                    # Status code details
protocolcodes search "redirect"             # Search codes
protocolcodes category 4xx                  # All client error codes
protocolcodes categories                    # List all categories
```

## MCP Server (Claude, Cursor, Windsurf)

```bash
pip install "protocolcodes[mcp]"
```

```json
{
    "mcpServers": {
        "protocolcodes": {
            "command": "uvx",
            "args": ["--from", "protocolcodes[mcp]", "python", "-m", "protocolcodes.mcp_server"]
        }
    }
}
```

## REST API Client

```python
from protocolcodes.api import ProtocolCodes

with ProtocolCodes() as api:
    code = api.get_status_code(404)                 # GET /api/v1/status-codes/404/
    codes = api.list_status_codes(category="4xx")    # GET /api/v1/status-codes/?category=4xx
    categories = api.list_categories()               # GET /api/v1/categories/
    results = api.search("teapot")                  # GET /api/v1/search/?q=teapot
```

### Example

```bash
curl -s "https://statuscodefyi.com/api/v1/status-codes/404/"
```

```json
{
    "code": 404,
    "phrase": "Not Found",
    "category": "4xx Client Error",
    "rfc": "RFC 9110",
    "description": "The server cannot find the requested resource."
}
```

Full API documentation at [statuscodefyi.com/developers/](https://statuscodefyi.com/developers/).

## API Reference

| Function | Description |
|----------|-------------|
| `api.get_status_code(code)` | Status code details (phrase, RFC, description) |
| `api.list_status_codes(category)` | List codes, optionally by category |
| `api.list_categories()` | All status code categories (1xx-5xx) |
| `api.get_category(slug)` | Category details with code list |
| `api.search(query)` | Search codes by number, phrase, or keyword |

## Learn More About HTTP

- **Browse**: [Status Codes](https://statuscodefyi.com/status-codes/) · [Categories](https://statuscodefyi.com/categories/)
- **Guides**: [HTTP Guides](https://statuscodefyi.com/guides/) · [Glossary](https://statuscodefyi.com/glossary/)
- **API**: [REST API Docs](https://statuscodefyi.com/developers/) · [OpenAPI Spec](https://statuscodefyi.com/api/openapi.json)

## Also Available

| Platform | Install | Link |
|----------|---------|------|
| **npm** | `npm install protocolcodes` | [npm](https://www.npmjs.com/package/protocolcodes) |
| **MCP** | `uvx --from "protocolcodes[mcp]" python -m protocolcodes.mcp_server` | [Config](#mcp-server-claude-cursor-windsurf) |

## Network FYI Family

Part of the [FYIPedia](https://fyipedia.com) open-source developer tools ecosystem — internet infrastructure, cables, domains, and protocols.

| Package | PyPI | npm | Description |
|---------|------|-----|-------------|
| cablefyi | [PyPI](https://pypi.org/project/cablefyi/) | [npm](https://www.npmjs.com/package/cablefyi) | Submarine cables, landing points, operators — [cablefyi.com](https://cablefyi.com/) |
| tldfyi | [PyPI](https://pypi.org/project/tldfyi/) | [npm](https://www.npmjs.com/package/tldfyi) | TLD registry, domain extensions, WHOIS — [tldfyi.com](https://tldfyi.com/) |
| ipfyi | [PyPI](https://pypi.org/project/ipfyi/) | [npm](https://www.npmjs.com/package/ipfyi) | IP geolocation, ASN lookup, CIDR ranges — [ipfyi.com](https://ipfyi.com/) |
| **protocolcodes** | [PyPI](https://pypi.org/project/protocolcodes/) | [npm](https://www.npmjs.com/package/protocolcodes) | **HTTP status codes, protocol references — [statuscodefyi.com](https://statuscodefyi.com/)** |

## License

MIT
