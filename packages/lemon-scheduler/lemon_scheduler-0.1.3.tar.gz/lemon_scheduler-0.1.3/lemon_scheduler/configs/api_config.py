from typing import Set

from pydantic import BaseModel


class RuntimeConfig(BaseModel):
    max_file_bytes: int = 1024 * 1024 * 4
    supported_file_types: Set[str] = {"txt"}


runtime_config: RuntimeConfig = RuntimeConfig()
