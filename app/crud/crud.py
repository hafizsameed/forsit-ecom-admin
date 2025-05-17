from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any, Union, Tuple
from datetime import datetime, date, timedelta
from sqlalchemy import func, desc, and_, or_, extract
from sqlalchemy.sql import label
import pandas as pd

from app.models.models import (
    Category,
    Product,
    Inventory,
    InventoryHistory,
    Sale,
    SaleItem,
    Customer,
)
from app.schemas import schemas


def create_category(db: Session, category: schemas.CategoryCreate) -> Category:
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_id: int) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_name(db: Session, name: str) -> Optional[Category]:
    return db.query(Category).filter(Category.name == name).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    return db.query(Category).offset(skip).limit(limit).all()


def update_category(
    db: Session, category_id: int, category: schemas.CategoryUpdate
) -> Optional[Category]:
    db_category = get_category(db, category_id)
    if db_category:
        update_data = category.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_category, field, value)
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int) -> bool:
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False


def create_product(db: Session, product: schemas.ProductCreate) -> Product:
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()


def get_product_by_sku(db: Session, sku: str) -> Optional[Product]:
    return db.query(Product).filter(Product.sku == sku).first()


def get_products(
    db: Session, skip: int = 0, limit: int = 100, category_id: Optional[int] = None
) -> List[Product]:
    query = db.query(Product)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    return query.offset(skip).limit(limit).all()


def update_product(
    db: Session, product_id: int, product: schemas.ProductUpdate
) -> Optional[Product]:
    db_product = get_product(db, product_id)
    if db_product:
        update_data = product.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> bool:
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False


def create_inventory(db: Session, inventory: schemas.InventoryCreate) -> Inventory:
    db_inventory = Inventory(**inventory.dict())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory


def get_inventory(db: Session, inventory_id: int) -> Optional[Inventory]:
    return db.query(Inventory).filter(Inventory.id == inventory_id).first()


def get_inventory_by_product(db: Session, product_id: int) -> Optional[Inventory]:
    return db.query(Inventory).filter(Inventory.product_id == product_id).first()


def get_inventories(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    low_stock_only: bool = False,
    category_id: Optional[int] = None,
) -> List[Inventory]:
    query = db.query(Inventory)

    if low_stock_only:
        query = query.filter(Inventory.quantity <= Inventory.low_stock_threshold)

    if category_id:
        query = query.join(Product).filter(Product.category_id == category_id)

    return query.offset(skip).limit(limit).all()


def update_inventory(
    db: Session,
    inventory_id: int,
    inventory_update: schemas.InventoryUpdate,
    change_reason: Optional[str] = None,
) -> Optional[Inventory]:
    db_inventory = get_inventory(db, inventory_id)

    if db_inventory:
        update_data = inventory_update.dict(exclude_unset=True)
        if (
            "quantity" in update_data
            and update_data["quantity"] != db_inventory.quantity
        ):
            previous_quantity = db_inventory.quantity
            new_quantity = update_data["quantity"]

            inventory_history = InventoryHistory(
                inventory_id=inventory_id,
                previous_quantity=previous_quantity,
                new_quantity=new_quantity,
                change_reason=change_reason,
            )
            db.add(inventory_history)

        for field, value in update_data.items():
            setattr(db_inventory, field, value)

        db.commit()
        db.refresh(db_inventory)

    return db_inventory


def get_inventory_history(
    db: Session, inventory_id: int, skip: int = 0, limit: int = 100
) -> List[InventoryHistory]:
    return (
        db.query(InventoryHistory)
        .filter(InventoryHistory.inventory_id == inventory_id)
        .order_by(desc(InventoryHistory.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_low_stock_alerts(
    db: Session, threshold_override: Optional[int] = None
) -> List[Dict[str, Any]]:
    query = db.query(
        Product.id.label("product_id"),
        Product.name.label("product_name"),
        Inventory.quantity.label("current_quantity"),
        Inventory.low_stock_threshold.label("threshold"),
    ).join(Inventory, Product.id == Inventory.product_id)

    if threshold_override:
        query = query.filter(Inventory.quantity <= threshold_override)
    else:
        query = query.filter(Inventory.quantity <= Inventory.low_stock_threshold)

    results = query.all()
    return [
        {
            "product_id": r.product_id,
            "product_name": r.product_name,
            "current_quantity": r.current_quantity,
            "threshold": r.threshold,
        }
        for r in results
    ]


def create_customer(db: Session, customer: schemas.CustomerCreate) -> Customer:
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def get_customer(db: Session, customer_id: int) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_customer_by_email(db: Session, email: str) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.email == email).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100) -> List[Customer]:
    return db.query(Customer).offset(skip).limit(limit).all()


def update_customer(
    db: Session, customer_id: int, customer: schemas.CustomerUpdate
) -> Optional[Customer]:
    db_customer = get_customer(db, customer_id)
    if db_customer:
        update_data = customer.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_customer, field, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer


def create_sale(db: Session, sale: schemas.SaleCreate) -> Sale:
    sale_dict = sale.dict(exclude={"items"})
    db_sale = Sale(**sale_dict)
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)

    for item in sale.items:
        db_sale_item = SaleItem(sale_id=db_sale.id, **item.dict())
        db.add(db_sale_item)
        db_inventory = get_inventory_by_product(db, item.product_id)
        if db_inventory:
            new_quantity = max(0, db_inventory.quantity - item.quantity)
            update_inventory(
                db,
                db_inventory.id,
                schemas.InventoryUpdate(quantity=new_quantity),
                f"Sale: {db_sale.order_number}",
            )

    db.commit()
    db.refresh(db_sale)
    return db_sale


def get_sale(db: Session, sale_id: int) -> Optional[Sale]:
    return db.query(Sale).filter(Sale.id == sale_id).first()


def get_sale_by_order_number(db: Session, order_number: str) -> Optional[Sale]:
    return db.query(Sale).filter(Sale.order_number == order_number).first()


def get_sales(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    customer_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    platform: Optional[str] = None,
) -> List[Sale]:
    query = db.query(Sale)

    if customer_id:
        query = query.filter(Sale.customer_id == customer_id)

    if start_date:
        query = query.filter(Sale.order_date >= start_date)

    if end_date:
        query = query.filter(Sale.order_date <= end_date)

    if platform:
        query = query.filter(Sale.platform == platform)

    return query.order_by(desc(Sale.order_date)).offset(skip).limit(limit).all()


def get_sale_items(db: Session, sale_id: int) -> List[SaleItem]:
    return db.query(SaleItem).filter(SaleItem.sale_id == sale_id).all()


def update_sale(db: Session, sale_id: int, sale: schemas.SaleUpdate) -> Optional[Sale]:
    db_sale = get_sale(db, sale_id)
    if db_sale:
        update_data = sale.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_sale, field, value)
        db.commit()
        db.refresh(db_sale)
    return db_sale

def get_sales_analytics(
    db: Session, params: schemas.SalesAnalyticsParams
) -> Dict[str, Any]:
    start_date = params.start_date
    end_date = params.end_date

    query = db.query(Sale).filter(
        Sale.order_date >= start_date, Sale.order_date <= end_date
    )

    if params.platform:
        query = query.filter(Sale.platform == params.platform)

    sales_data = query.all()

    if not sales_data:
        return {
            "total_sales": 0,
            "total_revenue": 0.0,
            "average_order_value": 0.0,
            "sales_by_date": {},
        }

    if params.product_id or params.category_id:
        filtered_sales = []

        for sale in sales_data:
            include_sale = False

            for item in sale.sale_items:
                if params.product_id and item.product_id == params.product_id:
                    include_sale = True
                    break

                if (
                    params.category_id
                    and item.product.category_id == params.category_id
                ):
                    include_sale = True
                    break

            if include_sale:
                filtered_sales.append(sale)

        sales_data = filtered_sales

    total_sales = len(sales_data)
    total_revenue = sum(sale.total_amount for sale in sales_data)
    average_order_value = total_revenue / total_sales if total_sales > 0 else 0.0

    sales_by_date = {}
    for sale in sales_data:
        sale_date = sale.order_date.date().isoformat()
        if sale_date not in sales_by_date:
            sales_by_date[sale_date] = {"count": 0, "revenue": 0.0}
        sales_by_date[sale_date]["count"] += 1
        sales_by_date[sale_date]["revenue"] += sale.total_amount

    return {
        "total_sales": total_sales,
        "total_revenue": total_revenue,
        "average_order_value": average_order_value,
        "sales_by_date": sales_by_date,
    }


def get_revenue_analytics(
    db: Session, params: schemas.RevenueAnalyticsParams
) -> Dict[str, Any]:
    start_date = params.start_date
    end_date = params.end_date
    group_by = params.group_by.lower()

    valid_group_by = ["day", "week", "month", "year"]
    if group_by not in valid_group_by:
        group_by = "day"

    query = db.query(Sale).filter(
        Sale.order_date >= start_date, Sale.order_date <= end_date
    )

    if params.platform:
        query = query.filter(Sale.platform == params.platform)

    if params.product_id:
        query = query.join(SaleItem).filter(SaleItem.product_id == params.product_id)

    if params.category_id:
        query = (
            query.join(SaleItem)
            .join(Product)
            .filter(Product.category_id == params.category_id)
        )

    sales_data = query.all()

    if not sales_data:
        return {"total_revenue": 0.0, "revenue_by_period": {}}

    df = pd.DataFrame(
        [
            {"order_date": sale.order_date, "total_amount": sale.total_amount}
            for sale in sales_data
        ]
    )

    if group_by == "day":
        df["period"] = df["order_date"].dt.date
    elif group_by == "week":
        df["period"] = (
            df["order_date"].dt.to_period("W").apply(lambda x: x.start_time.date())
        )
    elif group_by == "month":
        df["period"] = (
            df["order_date"].dt.to_period("M").apply(lambda x: x.start_time.date())
        )
    elif group_by == "year":
        df["period"] = df["order_date"].dt.year

    revenue_by_period = df.groupby("period")["total_amount"].sum().to_dict()

    revenue_by_period = {str(k): float(v) for k, v in revenue_by_period.items()}

    return {
        "total_revenue": float(df["total_amount"].sum()),
        "revenue_by_period": revenue_by_period,
    }


def get_inventory_analytics(
    db: Session, params: schemas.InventoryAnalyticsParams
) -> Dict[str, Any]:
    query = db.query(Inventory)

    if params.category_id:
        query = query.join(Product).filter(Product.category_id == params.category_id)

    inventories = query.all()

    total_products = len(inventories)
    out_of_stock_products = sum(1 for inv in inventories if inv.quantity == 0)

    low_stock_products = []
    for inv in inventories:
        if params.low_stock_only and inv.quantity > inv.low_stock_threshold:
            continue

        if inv.quantity <= inv.low_stock_threshold:
            low_stock_products.append(
                {
                    "product_id": inv.product_id,
                    "product_name": inv.product.name,
                    "current_quantity": inv.quantity,
                    "threshold": inv.low_stock_threshold,
                }
            )

    return {
        "total_products": total_products,
        "out_of_stock_products": out_of_stock_products,
        "low_stock_alerts": low_stock_products,
    }


def compare_revenue_periods(
    db: Session,
    current_start: date,
    current_end: date,
    previous_start: date,
    previous_end: date,
    group_by: str = "day",
    product_id: Optional[int] = None,
    category_id: Optional[int] = None,
    platform: Optional[str] = None,
) -> Dict[str, Any]:
    current_params = schemas.RevenueAnalyticsParams(
        start_date=current_start,
        end_date=current_end,
        group_by=group_by,
        product_id=product_id,
        category_id=category_id,
        platform=platform,
    )
    current_revenue = get_revenue_analytics(db, current_params)

    previous_params = schemas.RevenueAnalyticsParams(
        start_date=previous_start,
        end_date=previous_end,
        group_by=group_by,
        product_id=product_id,
        category_id=category_id,
        platform=platform,
    )
    previous_revenue = get_revenue_analytics(db, previous_params)

    current_total = current_revenue["total_revenue"]
    previous_total = previous_revenue["total_revenue"]

    if previous_total > 0:
        percent_change = ((current_total - previous_total) / previous_total) * 100
    else:
        percent_change = float("inf") if current_total > 0 else 0

    return {
        "current_period": {
            "start_date": current_start.isoformat(),
            "end_date": current_end.isoformat(),
            "total_revenue": current_total,
            "revenue_by_period": current_revenue["revenue_by_period"],
        },
        "previous_period": {
            "start_date": previous_start.isoformat(),
            "end_date": previous_end.isoformat(),
            "total_revenue": previous_total,
            "revenue_by_period": previous_revenue["revenue_by_period"],
        },
        "comparison": {
            "absolute_change": current_total - previous_total,
            "percent_change": percent_change,
        },
    }
