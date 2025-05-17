from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any, List, Optional
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.models.models import Sale, Product, Inventory, Category, SaleItem
from app.crud.crud import (
    get_sales_analytics,
    get_revenue_analytics,
    get_inventory_analytics,
    compare_revenue_periods,
)
from app.schemas.schemas import (
    SalesAnalyticsParams,
    RevenueAnalyticsParams,
    InventoryAnalyticsParams,
)


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
async def get_dashboard_summary(
    period_days: int = Query(30, ge=1, le=365), db: Session = Depends(get_db)
):
    today = datetime.now().date()
    start_date = today - timedelta(days=period_days)
    sales_params = SalesAnalyticsParams(start_date=start_date, end_date=today)
    sales_data = get_sales_analytics(db, sales_params)
    revenue_params = RevenueAnalyticsParams(
        start_date=start_date, end_date=today, group_by="day"
    )
    revenue_data = get_revenue_analytics(db, revenue_params)
    inventory_params = InventoryAnalyticsParams(low_stock_only=True)
    inventory_data = get_inventory_analytics(db, inventory_params)
    prev_start_date = start_date - timedelta(days=period_days)
    prev_end_date = today - timedelta(days=period_days)

    comparison = compare_revenue_periods(
        db,
        current_start=start_date,
        current_end=today,
        previous_start=prev_start_date,
        previous_end=prev_end_date,
        group_by="day",
    )

    top_products_query = (
        db.query(
            Product.id,
            Product.name,
            func.sum(SaleItem.quantity).label("total_sold"),
            func.sum(SaleItem.unit_price * SaleItem.quantity - SaleItem.discount).label(
                "total_revenue"
            ),
        )
        .join(SaleItem)
        .join(Sale)
        .filter(Sale.order_date >= start_date, Sale.order_date <= today)
        .group_by(Product.id)
        .order_by(func.sum(SaleItem.quantity).desc())
        .limit(5)
    )

    top_products = [
        {
            "id": p.id,
            "name": p.name,
            "total_sold": p.total_sold,
            "total_revenue": float(p.total_revenue),
        }
        for p in top_products_query.all()
    ]

    platform_query = (
        db.query(
            Sale.platform,
            func.count(Sale.id).label("order_count"),
            func.sum(Sale.total_amount).label("total_revenue"),
        )
        .filter(Sale.order_date >= start_date, Sale.order_date <= today)
        .group_by(Sale.platform)
        .order_by(func.sum(Sale.total_amount).desc())
    )

    platform_distribution = [
        {
            "platform": p.platform,
            "order_count": p.order_count,
            "total_revenue": float(p.total_revenue),
        }
        for p in platform_query.all()
    ]

    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": today.isoformat(),
            "days": period_days,
        },
        "sales_summary": {
            "total_orders": sales_data["total_sales"],
            "average_order_value": sales_data["average_order_value"],
        },
        "revenue_summary": {
            "total_revenue": revenue_data["total_revenue"],
            "revenue_change_percent": comparison["comparison"]["percent_change"],
        },
        "inventory_summary": {
            "total_products": inventory_data["total_products"],
            "out_of_stock": inventory_data["out_of_stock_products"],
            "low_stock_alerts": len(inventory_data["low_stock_alerts"]),
        },
        "top_products": top_products,
        "platform_distribution": platform_distribution,
    }
