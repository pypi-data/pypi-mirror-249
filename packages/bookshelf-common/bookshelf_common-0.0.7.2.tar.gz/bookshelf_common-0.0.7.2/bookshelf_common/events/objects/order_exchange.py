from dataclasses import dataclass, asdict
import json

@dataclass
class OrderExchange:
  order_id: int
  book_id: int
  status: str = 'await_payment'

  @property
  def subject(self) -> str:
    return 'order_exchange'
  
  @property
  def message_body(self) -> str:
    return json.dumps(asdict(self))

  @classmethod
  def parse_message(cls, msg):
    data = json.loads(msg)
    return cls(**data)