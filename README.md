
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
from logicipi import gcp_logger

log = gcp_logger("my-function-name").logger
log.info("Hello There")

```

The `auth` flow relys on the GCloud Auth flow, you can read more [here](https://googleapis.dev/python/google-api-core/latest/auth.html)
