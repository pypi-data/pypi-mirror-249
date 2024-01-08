from dataclasses import dataclass, asdict
import json

@dataclass
class BookSold:
  payment_id: int
  order_id: int
  buyer_id: int
  buyer_email: str
  buyer_phone: str
  sellers_id: int
  sellers_email: str
  sellers_phone: str
  book_id: int
  book_title: str
  book_author: str

  @property
  def subject(self) -> str:
    return 'book_sold'
  
  @property
  def message_body(self) -> str:
    return json.dumps(asdict(self))

  @classmethod
  def parse_message(cls, msg):
    data = json.loads(msg)
    return cls(**data)