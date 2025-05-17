from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta

from app.db.session import get_db
from app.schemas import schemas
from app.crud import crud


router = APIRouter()


@router.post("/categories/", response_model=schemas.Category, status_code=201)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_name(db, name=category.name)
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    return crud.create_category(db=db, category=category)


@router.get("/categories/", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories


@router.get("/categories/{category_id}", response_model=schemas.Category)
def read_category(
    category_id: int = Path(..., title="The ID of the category to get"),
    db: Session = Depends(get_db),
):
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.put("/categories/{category_id}", response_model=schemas.Category)
def update_category(
    category_id: int = Path(..., title="The ID of the category to update"),
    category: schemas.CategoryUpdate = None,
    db: Session = Depends(get_db),
):
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.update_category(db=db, category_id=category_id, category=category)


@router.delete("/categories/{category_id}", response_model=bool)
def delete_category(
    category_id: int = Path(..., title="The ID of the category to delete"),
    db: Session = Depends(get_db),
):
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.delete_category(db=db, category_id=category_id)


@router.post("/products/", response_model=schemas.Product, status_code=201)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    if crud.get_product_by_sku(db, sku=product.sku):
        raise HTTPException(status_code=400, detail="SKU already registered")

    if not crud.get_category(db, category_id=product.category_id):
        raise HTTPException(status_code=404, detail="Category not found")

    return crud.create_product(db=db, product=product)


@router.get("/products/", response_model=List[schemas.Product])
def read_products(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    products = crud.get_products(db, skip=skip, limit=limit, category_id=category_id)
    return products


@router.get("/products/{product_id}", response_model=schemas.Product)
def read_product(
    product_id: int = Path(..., title="The ID of the product to get"),
    db: Session = Depends(get_db),
):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.put("/products/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int = Path(..., title="The ID of the product to update"),
    product: schemas.ProductUpdate = None,
    db: Session = Depends(get_db),
):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.category_id and not crud.get_category(
        db, category_id=product.category_id
    ):
        raise HTTPException(status_code=404, detail="Category not found")

    return crud.update_product(db=db, product_id=product_id, product=product)


@router.delete("/products/{product_id}", response_model=bool)
def delete_product(
    product_id: int = Path(..., title="The ID of the product to delete"),
    db: Session = Depends(get_db),
):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.delete_product(db=db, product_id=product_id)


@router.post("/inventory/", response_model=schemas.Inventory, status_code=201)
def create_inventory(inventory: schemas.InventoryCreate, db: Session = Depends(get_db)):
    if not crud.get_product(db, product_id=inventory.product_id):
        raise HTTPException(status_code=404, detail="Product not found")

    if crud.get_inventory_by_product(db, product_id=inventory.product_id):
        raise HTTPException(
            status_code=400, detail="Inventory for this product already exists"
        )

    return crud.create_inventory(db=db, inventory=inventory)


@router.get("/inventory/", response_model=List[schemas.Inventory])
def read_inventories(
    skip: int = 0,
    limit: int = 100,
    low_stock_only: bool = False,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    inventories = crud.get_inventories(
        db,
        skip=skip,
        limit=limit,
        low_stock_only=low_stock_only,
        category_id=category_id,
    )
    return inventories


@router.get("/inventory/{inventory_id}", response_model=schemas.Inventory)
def read_inventory(
    inventory_id: int = Path(..., title="The ID of the inventory to get"),
    db: Session = Depends(get_db),
):
    db_inventory = crud.get_inventory(db, inventory_id=inventory_id)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return db_inventory


@router.get("/inventory/product/{product_id}", response_model=schemas.Inventory)
def read_inventory_by_product(
    product_id: int = Path(..., title="The ID of the product to get inventory for"),
    db: Session = Depends(get_db),
):
    db_inventory = crud.get_inventory_by_product(db, product_id=product_id)
    if db_inventory is None:
        raise HTTPException(
            status_code=404, detail="Inventory not found for this product"
        )
    return db_inventory


@router.put("/inventory/{inventory_id}", response_model=schemas.Inventory)
def update_inventory(
    inventory_id: int = Path(..., title="The ID of the inventory to update"),
    inventory: schemas.InventoryUpdate = None,
    change_reason: Optional[str] = Query(
        None, description="Reason for inventory change"
    ),
    db: Session = Depends(get_db),
):
    db_inventory = crud.get_inventory(db, inventory_id=inventory_id)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")

    return crud.update_inventory(
        db=db,
        inventory_id=inventory_id,
        inventory_update=inventory,
        change_reason=change_reason,
    )


@router.get(
    "/inventory/{inventory_id}/history", response_model=List[schemas.InventoryHistory]
)
def read_inventory_history(
    inventory_id: int = Path(..., title="The ID of the inventory to get history for"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if not crud.get_inventory(db, inventory_id=inventory_id):
        raise HTTPException(status_code=404, detail="Inventory not found")

    history = crud.get_inventory_history(
        db, inventory_id=inventory_id, skip=skip, limit=limit
    )
    return history


@router.get("/inventory/low-stock", response_model=List[schemas.LowStockAlert])
def get_low_stock_alerts(
    threshold_override: Optional[int] = Query(
        None, description="Override the default low stock threshold"
    ),
    db: Session = Depends(get_db),
):
    alerts = crud.get_low_stock_alerts(db, threshold_override=threshold_override)
    return alerts


@router.post("/customers/", response_model=schemas.Customer, status_code=201)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db=db, customer=customer)


@router.get("/customers/", response_model=List[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers


@router.get("/customers/{customer_id}", response_model=schemas.Customer)
def read_customer(
    customer_id: int = Path(..., title="The ID of the customer to get"),
    db: Session = Depends(get_db),
):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


@router.put("/customers/{customer_id}", response_model=schemas.Customer)
def update_customer(
    customer_id: int = Path(..., title="The ID of the customer to update"),
    customer: schemas.CustomerUpdate = None,
    db: Session = Depends(get_db),
):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.update_customer(db=db, customer_id=customer_id, customer=customer)


@router.post("/sales/", response_model=schemas.Sale, status_code=201)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    if not crud.get_customer(db, customer_id=sale.customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")

    for item in sale.items:
        if not crud.get_product(db, product_id=item.product_id):
            raise HTTPException(
                status_code=404, detail=f"Product with ID {item.product_id} not found"
            )

        inventory = crud.get_inventory_by_product(db, product_id=item.product_id)
        if not inventory:
            raise HTTPException(
                status_code=404,
                detail=f"Inventory not found for product with ID {item.product_id}",
            )

        if inventory.quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product with ID {item.product_id}",
            )

    return crud.create_sale(db=db, sale=sale)


@router.get("/sales/", response_model=List[schemas.Sale])
def read_sales(
    skip: int = 0,
    limit: int = 100,
    customer_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    platform: Optional[str] = None,
    db: Session = Depends(get_db),
):
    sales = crud.get_sales(
        db,
        skip=skip,
        limit=limit,
        customer_id=customer_id,
        start_date=start_date,
        end_date=end_date,
        platform=platform,
    )
    return sales


@router.get("/sales/{sale_id}", response_model=schemas.Sale)
def read_sale(
    sale_id: int = Path(..., title="The ID of the sale to get"),
    db: Session = Depends(get_db),
):
    db_sale = crud.get_sale(db, sale_id=sale_id)
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_sale


@router.get("/sales/order/{order_number}", response_model=schemas.Sale)
def read_sale_by_order_number(
    order_number: str = Path(..., title="The order number of the sale to get"),
    db: Session = Depends(get_db),
):
    db_sale = crud.get_sale_by_order_number(db, order_number=order_number)
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_sale


@router.put("/sales/{sale_id}", response_model=schemas.Sale)
def update_sale(
    sale_id: int = Path(..., title="The ID of the sale to update"),
    sale: schemas.SaleUpdate = None,
    db: Session = Depends(get_db),
):
    db_sale = crud.get_sale(db, sale_id=sale_id)
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return crud.update_sale(db=db, sale_id=sale_id, sale=sale)


@router.post("/analytics/sales", response_model=schemas.SalesAnalyticsResponse)
def get_sales_analytics(
    params: schemas.SalesAnalyticsParams, db: Session = Depends(get_db)
):
    return crud.get_sales_analytics(db=db, params=params)


@router.post("/analytics/revenue", response_model=schemas.RevenueAnalyticsResponse)
def get_revenue_analytics(
    params: schemas.RevenueAnalyticsParams, db: Session = Depends(get_db)
):
    return crud.get_revenue_analytics(db=db, params=params)


@router.post("/analytics/inventory", response_model=schemas.InventoryAnalyticsResponse)
def get_inventory_analytics(
    params: schemas.InventoryAnalyticsParams, db: Session = Depends(get_db)
):
    return crud.get_inventory_analytics(db=db, params=params)


@router.post("/analytics/revenue/compare")
def compare_revenue(
    current_start: date,
    current_end: date,
    previous_start: Optional[date] = None,
    previous_end: Optional[date] = None,
    group_by: str = "day",
    product_id: Optional[int] = None,
    category_id: Optional[int] = None,
    platform: Optional[str] = None,
    db: Session = Depends(get_db),
):
    # If previous dates are not provided, calculate them
    if previous_start is None or previous_end is None:
        # Calculate the duration of the current period
        current_duration = (current_end - current_start).days + 1

        # Set previous period to be the same duration immediately before the current period
        if previous_end is None:
            previous_end = current_start - timedelta(days=1)

        if previous_start is None:
            previous_start = previous_end - timedelta(days=current_duration - 1)

    return crud.compare_revenue_periods(
        db,
        current_start=current_start,
        current_end=current_end,
        previous_start=previous_start,
        previous_end=previous_end,
        group_by=group_by,
        product_id=product_id,
        category_id=category_id,
        platform=platform,
    )
