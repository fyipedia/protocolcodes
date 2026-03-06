# protocolcodes

HTTP status codes and protocol reference API client — [protocolcodes.com](https://protocolcodes.com)

## Install

```bash
pip install protocolcodes
```

## Quick Start

```python
from protocolcodes.api import ProtocolCodes

with ProtocolCodes() as api:
    results = api.search("404")
    print(results)
```

## License

MIT
