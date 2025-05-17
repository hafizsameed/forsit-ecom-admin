import os
import sys
import json
from datetime import datetime, timedelta
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal
from app.schemas.schemas import (
    SalesAnalyticsParams,
    RevenueAnalyticsParams,
    InventoryAnalyticsParams,
)
from app.crud.crud import (
    get_categories,
    get_products,
    get_inventories,
    get_sales,
    get_sales_analytics,
    get_revenue_analytics,
    get_inventory_analytics,
    compare_revenue_periods,
)


def export_sample_responses():
    output_dir = os.path.join(os.path.dirname(__file__), "..", "mock_data")
    os.makedirs(output_dir, exist_ok=True)

    db = SessionLocal()
    today = datetime.now().date()

    try:
        thirty_days_ago = today - timedelta(days=30)
        sixty_days_ago = today - timedelta(days=60)

        categories = get_categories(db)
        export_json(
            output_dir,
            "categories.json",
            [
                {"id": c.id, "name": c.name, "description": c.description}
                for c in categories
            ],
        )

        products = get_products(db, limit=10)
        export_json(
            output_dir,
            "products_sample.json",
            [
                {
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                    "sku": p.sku,
                    "price": p.price,
                    "category_id": p.category_id,
                    "category": {"id": p.category.id, "name": p.category.name},
                }
                for p in products
            ],
        )

        inventories = get_inventories(db, limit=10)
        export_json(
            output_dir,
            "inventory_sample.json",
            [
                {
                    "id": i.id,
                    "product_id": i.product_id,
                    "product_name": i.product.name,
                    "quantity": i.quantity,
                    "low_stock_threshold": i.low_stock_threshold,
                    "last_restock_date": (
                        i.last_restock_date.isoformat() if i.last_restock_date else None
                    ),
                }
                for i in inventories
            ],
        )

        sales = get_sales(db, limit=10)
        export_json(
            output_dir,
            "sales_sample.json",
            [
                {
                    "id": s.id,
                    "order_number": s.order_number,
                    "order_date": s.order_date.isoformat(),
                    "customer_name": s.customer.name,
                    "total_amount": s.total_amount,
                    "platform": s.platform,
                    "status": s.status,
                    "items_count": len(s.sale_items),
                }
                for s in sales
            ],
        )

        sales_params = SalesAnalyticsParams(start_date=thirty_days_ago, end_date=today)
        sales_analytics = get_sales_analytics(db, sales_params)
        export_json(output_dir, "sales_analytics_30d.json", sales_analytics)

        revenue_params = RevenueAnalyticsParams(
            start_date=thirty_days_ago, end_date=today, group_by="day"
        )
        revenue_analytics = get_revenue_analytics(db, revenue_params)
        export_json(output_dir, "revenue_analytics_30d.json", revenue_analytics)

        revenue_params_week = RevenueAnalyticsParams(
            start_date=thirty_days_ago, end_date=today, group_by="week"
        )
        revenue_analytics_week = get_revenue_analytics(db, revenue_params_week)
        export_json(
            output_dir, "revenue_analytics_30d_weekly.json", revenue_analytics_week
        )

        comparison = compare_revenue_periods(
            db,
            current_start=thirty_days_ago,
            current_end=today,
            previous_start=sixty_days_ago,
            previous_end=thirty_days_ago,
            group_by="day",
        )
        export_json(output_dir, "revenue_comparison_30d.json", comparison)

        inventory_params = InventoryAnalyticsParams(low_stock_only=False)
        inventory_analytics = get_inventory_analytics(db, inventory_params)
        export_json(output_dir, "inventory_analytics.json", inventory_analytics)

        inventory_params_low = InventoryAnalyticsParams(low_stock_only=True)
        inventory_analytics_low = get_inventory_analytics(db, inventory_params_low)
        export_json(output_dir, "low_stock_alerts.json", inventory_analytics_low)

        print(f"Sample data exported to {output_dir}")

    finally:
        db.close()


def export_json(directory, filename, data):
    file_path = os.path.join(directory, filename)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"Exported {filename}")


if __name__ == "__main__":
    export_sample_responses()
