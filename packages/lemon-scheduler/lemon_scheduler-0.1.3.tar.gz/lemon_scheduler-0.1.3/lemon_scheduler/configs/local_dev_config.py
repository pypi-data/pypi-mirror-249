import os.path
from typing import Optional

from pydantic import BaseModel

from settings import BASE_DIR


class LemonClientConfig(BaseModel):
    base_url: str
    app_uuid: str
    module_uuid: str
    username: str
    tenant_uuid: str
    password: str


class LocalDEVConfig(BaseModel):
    lemon_scheduler: LemonClientConfig


config: Optional[LocalDEVConfig] = None
dev_config_path = os.path.join(BASE_DIR, "local_dev_config.json")
if os.path.exists(dev_config_path):
    config = LocalDEVConfig.parse_file(dev_config_path)
