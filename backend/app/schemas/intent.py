from pydantic import BaseModel

class Intent(BaseModel):
  place_order: str = "place_order"
  track_order: str = "track_order"
  cancel_order: str = "cancel_order"
  support_ticket: str = "support_ticket"
  schedule_meet: int = "schedule_meet"
  product_service_price: str = "product_service_price"
  product_service_info: str = "product_service_info"