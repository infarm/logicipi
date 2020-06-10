
# LoGiCiPi

A tiny wrapper on structlog and gcloud logging library for applications running inside GCP.

Works for both cloud functions and containers.

## Quickstart

### Containers

LoGiCiPi provides a nice util, `configure_structlog`, with a pre-configured logging.

You only need to import it and then run it.

```python
from logicipi import configure_structlog
from structlog import get_logger

configure_structlog()

log = get_logger()

log.info("Hi There")
# {"event": "Hello There", "logger": "__main__", "timestamp": "2020-06-09T13:24:43.481664Z", "severity": "info"}
```

### Cloud functions

```python

# file main.py
from logicipi import gcp_logger

log = gcp_logger(function_name="my-function-name", region="my-region").get_logger()

log.info("Hello There", value=1)

# file another.py
from logicipi import gcp_logger

log = gcp_logger().get_logger()

log.error("Hello There", value=1)
```

`gcp_logger` returns a singleton, so the object can be instantiated only once.

The `auth` flow relies on the GCloud Auth flow, you can read more [here](https://googleapis.dev/python/google-api-core/latest/auth.html).
