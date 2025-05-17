from typing import List, Optional, Union, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field, EmailStr


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: Optional[str] = None


class CategoryInDB(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Category(CategoryInDB):
    pass


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    sku: str
    price: float
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None


class ProductInDB(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Product(ProductInDB):
    category: Category


class InventoryBase(BaseModel):
    product_id: int
    quantity: int
    location: Optional[str] = None
    low_stock_threshold: int = 10


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    quantity: Optional[int] = None
    location: Optional[str] = None
    low_stock_threshold: Optional[int] = None
    last_restock_date: Optional[datetime] = None


class InventoryInDB(InventoryBase):
    id: int
    last_restock_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Inventory(InventoryInDB):
    product: Product


class InventoryHistoryBase(BaseModel):
    inventory_id: int
    previous_quantity: int
    new_quantity: int
    change_reason: Optional[str] = None


class InventoryHistoryCreate(InventoryHistoryBase):
    pass


class InventoryHistoryInDB(InventoryHistoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class InventoryHistory(InventoryHistoryInDB):
    pass


class CustomerBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    name: Optional[str] = None


class CustomerInDB(CustomerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Customer(CustomerInDB):
    pass


class SaleItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    discount: float = 0


class SaleItemCreate(SaleItemBase):
    pass


class SaleItemInDB(SaleItemBase):
    id: int
    sale_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class SaleItem(SaleItemInDB):
    product: Product


class SaleBase(BaseModel):
    order_number: str
    order_date: datetime
    customer_id: int
    total_amount: float
    platform: str = "website"
    status: str = "completed"


class SaleCreate(SaleBase):
    items: List[SaleItemCreate]


class SaleUpdate(BaseModel):
    status: Optional[str] = None
    total_amount: Optional[float] = None


class SaleInDB(SaleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Sale(SaleInDB):
    customer: Customer
    sale_items: List[SaleItem]


class DateRangeParams(BaseModel):
    start_date: date
    end_date: date


class SalesAnalyticsParams(DateRangeParams):
    product_id: Optional[int] = None
    category_id: Optional[int] = None
    platform: Optional[str] = None


class RevenueAnalyticsParams(DateRangeParams):
    group_by: str = "day"
    product_id: Optional[int] = None
    category_id: Optional[int] = None
    platform: Optional[str] = None


class InventoryAnalyticsParams(BaseModel):
    low_stock_only: bool = False
    category_id: Optional[int] = None


class SalesAnalyticsResponse(BaseModel):
    total_sales: int
    total_revenue: float
    average_order_value: float
    sales_by_date: Dict[str, Any]


class RevenueAnalyticsResponse(BaseModel):
    total_revenue: float
    revenue_by_period: Dict[str, float]


class LowStockAlert(BaseModel):
    product_id: int
    product_name: str
    current_quantity: int
    threshold: int


class InventoryAnalyticsResponse(BaseModel):
    total_products: int
    out_of_stock_products: int
    low_stock_alerts: List[LowStockAlert]
