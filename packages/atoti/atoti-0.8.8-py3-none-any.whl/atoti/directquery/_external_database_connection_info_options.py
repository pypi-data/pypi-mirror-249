from datetime import timedelta
from typing import Literal

LookupMode = Literal["allow", "warn", "deny"]

DEFAULT_LOOKUP_MODE: LookupMode = "warn"
DEFAULT_MAX_SUB_QUERIES = 50
DEFAULT_QUERY_TIMEOUT = timedelta(hours=1)
