from dataclasses import dataclass, asdict
import json

@dataclass
class BookStatusExchange:
  id: int
  status: str
  status_msg: str
  msg_type: str

  @property
  def subject(self) -> str:
    return 'book_status_exchange'
  
  @property
  def message_body(self) -> str:
    return json.dumps(asdict(self))
  
  @classmethod
  def parse_message(cls, msg):
    data = json.loads(msg)
    return cls(**data)