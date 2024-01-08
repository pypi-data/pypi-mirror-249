from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class QueueList:
  exchange_subject: str
  queue_subject: str
  callback: Callable[..., None]

