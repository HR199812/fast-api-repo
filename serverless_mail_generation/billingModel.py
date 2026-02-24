from pydantic import BaseModel, EmailStr, Field, ConfigDict, BeforeValidator
from typing import List, Optional, Annotated
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]

class BillingItem(BaseModel):
    description: str
    quantity: int
    unit_price: float
    total: float


class CustomerInfo(BaseModel):
    name: str
    email: EmailStr
    address: str


class BillingSummary(BaseModel):
    subtotal: float
    tax_rate: float
    tax_amount: float
    total_amount: float


class InvoiceDocument(BaseModel):
    id: str = Field(alias="_id")
    invoice_number: str
    customer: CustomerInfo
    billing_date: datetime
    items: List[BillingItem]
    summary: BillingSummary
    currency: str = "INR"
    status: str = "draft"

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
