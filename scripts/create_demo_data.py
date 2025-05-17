import os
import sys
import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.orm import Session
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal
from app.models.models import (
    Category,
    Product,
    Inventory,
    Customer,
    Sale,
    SaleItem,
    Base,
    engine,
)
from app.schemas import schemas

load_dotenv()

fake = Faker()


def create_categories() -> list:
    categories = [
        {"name": "Electronics", "description": "Electronic devices and gadgets"},
        {"name": "Clothing", "description": "Apparel and fashion items"},
        {"name": "Home & Kitchen", "description": "Household items and appliances"},
        {"name": "Books", "description": "Books, e-books, and audiobooks"},
        {
            "name": "Sports & Outdoors",
            "description": "Sporting gear and outdoor equipment",
        },
        {
            "name": "Beauty & Personal Care",
            "description": "Cosmetics and personal care products",
        },
        {"name": "Toys & Games", "description": "Toys, games, and entertainment items"},
        {"name": "Grocery", "description": "Food and grocery items"},
    ]

    db_categories = []
    db = SessionLocal()

    try:
        for cat_data in categories:
            category = Category(**cat_data)
            db.add(category)
            db_categories.append(category)
        db.commit()

        for cat in db_categories:
            db.refresh(cat)
    finally:
        db.close()

    return db_categories


def create_products(categories: list) -> list:
    db_products = []
    db = SessionLocal()

    electronics_products = [
        {
            "name": "Smartphone X",
            "description": "Latest smartphone with advanced features",
            "price": 999.99,
            "sku": "ELEC-001",
        },
        {
            "name": "Laptop Pro",
            "description": "High-performance laptop for professionals",
            "price": 1299.99,
            "sku": "ELEC-002",
        },
        {
            "name": "Wireless Earbuds",
            "description": "True wireless earbuds with noise cancellation",
            "price": 149.99,
            "sku": "ELEC-003",
        },
        {
            "name": "Smart Watch",
            "description": "Fitness and health tracking smartwatch",
            "price": 249.99,
            "sku": "ELEC-004",
        },
        {
            "name": "4K Smart TV",
            "description": "Ultra HD smart television with streaming capabilities",
            "price": 799.99,
            "sku": "ELEC-005",
        },
    ]

    clothing_products = [
        {
            "name": "Men's T-Shirt",
            "description": "Cotton crew neck t-shirt",
            "price": 19.99,
            "sku": "CLTH-001",
        },
        {
            "name": "Women's Jeans",
            "description": "Slim fit denim jeans",
            "price": 49.99,
            "sku": "CLTH-002",
        },
        {
            "name": "Winter Jacket",
            "description": "Insulated water-resistant jacket",
            "price": 89.99,
            "sku": "CLTH-003",
        },
        {
            "name": "Athletic Shoes",
            "description": "High-performance running shoes",
            "price": 79.99,
            "sku": "CLTH-004",
        },
        {
            "name": "Casual Dress",
            "description": "Everyday casual dress",
            "price": 59.99,
            "sku": "CLTH-005",
        },
    ]

    home_products = [
        {
            "name": "Coffee Maker",
            "description": "Programmable coffee machine",
            "price": 69.99,
            "sku": "HOME-001",
        },
        {
            "name": "Blender",
            "description": "High-speed countertop blender",
            "price": 49.99,
            "sku": "HOME-002",
        },
        {
            "name": "Bed Sheets Set",
            "description": "100% cotton sheet set",
            "price": 39.99,
            "sku": "HOME-003",
        },
        {
            "name": "Cookware Set",
            "description": "Non-stick cooking set",
            "price": 129.99,
            "sku": "HOME-004",
        },
        {
            "name": "Table Lamp",
            "description": "Modern desk lamp with LED bulb",
            "price": 34.99,
            "sku": "HOME-005",
        },
    ]

    books_products = [
        {
            "name": "Fiction Bestseller",
            "description": "Top-selling novel",
            "price": 14.99,
            "sku": "BOOK-001",
        },
        {
            "name": "Cookbook",
            "description": "Recipe collection for home cooks",
            "price": 24.99,
            "sku": "BOOK-002",
        },
        {
            "name": "Self-Help Guide",
            "description": "Personal development book",
            "price": 19.99,
            "sku": "BOOK-003",
        },
        {
            "name": "Children's Story",
            "description": "Illustrated children's book",
            "price": 9.99,
            "sku": "BOOK-004",
        },
        {
            "name": "Business Strategy",
            "description": "Guide for entrepreneurs",
            "price": 29.99,
            "sku": "BOOK-005",
        },
    ]

    sports_products = [
        {
            "name": "Yoga Mat",
            "description": "Non-slip exercise mat",
            "price": 29.99,
            "sku": "SPRT-001",
        },
        {
            "name": "Dumbbell Set",
            "description": "Adjustable weight dumbbell pair",
            "price": 119.99,
            "sku": "SPRT-002",
        },
        {
            "name": "Tennis Racket",
            "description": "Professional tennis racket",
            "price": 89.99,
            "sku": "SPRT-003",
        },
        {
            "name": "Basketball",
            "description": "Official size basketball",
            "price": 29.99,
            "sku": "SPRT-004",
        },
        {
            "name": "Hiking Backpack",
            "description": "Durable outdoor backpack",
            "price": 69.99,
            "sku": "SPRT-005",
        },
    ]

    beauty_products = [
        {
            "name": "Face Moisturizer",
            "description": "Hydrating face cream",
            "price": 24.99,
            "sku": "BEAU-001",
        },
        {
            "name": "Shampoo",
            "description": "Volumizing hair shampoo",
            "price": 12.99,
            "sku": "BEAU-002",
        },
        {
            "name": "Perfume",
            "description": "Luxury fragrance",
            "price": 79.99,
            "sku": "BEAU-003",
        },
        {
            "name": "Makeup Set",
            "description": "Complete makeup collection",
            "price": 49.99,
            "sku": "BEAU-004",
        },
        {
            "name": "Electric Razor",
            "description": "Rechargeable grooming tool",
            "price": 59.99,
            "sku": "BEAU-005",
        },
    ]

    toys_products = [
        {
            "name": "Building Blocks",
            "description": "Creative construction set",
            "price": 24.99,
            "sku": "TOYS-001",
        },
        {
            "name": "Board Game",
            "description": "Family strategy game",
            "price": 34.99,
            "sku": "TOYS-002",
        },
        {
            "name": "Action Figure",
            "description": "Collectible character figure",
            "price": 19.99,
            "sku": "TOYS-003",
        },
        {
            "name": "Remote Control Car",
            "description": "High-speed RC vehicle",
            "price": 49.99,
            "sku": "TOYS-004",
        },
        {
            "name": "Stuffed Animal",
            "description": "Soft plush toy",
            "price": 14.99,
            "sku": "TOYS-005",
        },
    ]

    grocery_products = [
        {
            "name": "Coffee Beans",
            "description": "Premium roasted coffee",
            "price": 14.99,
            "sku": "GROC-001",
        },
        {
            "name": "Olive Oil",
            "description": "Extra virgin olive oil",
            "price": 19.99,
            "sku": "GROC-002",
        },
        {
            "name": "Organic Honey",
            "description": "Pure natural honey",
            "price": 9.99,
            "sku": "GROC-003",
        },
        {
            "name": "Pasta Set",
            "description": "Assorted Italian pasta",
            "price": 12.99,
            "sku": "GROC-004",
        },
        {
            "name": "Chocolate Box",
            "description": "Gourmet chocolate assortment",
            "price": 24.99,
            "sku": "GROC-005",
        },
    ]

    category_products = {
        "Electronics": electronics_products,
        "Clothing": clothing_products,
        "Home & Kitchen": home_products,
        "Books": books_products,
        "Sports & Outdoors": sports_products,
        "Beauty & Personal Care": beauty_products,
        "Toys & Games": toys_products,
        "Grocery": grocery_products,
    }

    try:
        cat_dict = {cat.name: cat for cat in categories}

        for cat_name, products_list in category_products.items():
            category_id = cat_dict[cat_name].id

            for product_data in products_list:
                product = Product(**product_data, category_id=category_id)
                db.add(product)
                db_products.append(product)

        db.commit()

        for product in db_products:
            db.refresh(product)
    finally:
        db.close()

    return db_products


def create_inventory(products: list) -> list:
    db_inventories = []
    db = SessionLocal()

    try:
        for product in products:
            quantity = random.randint(5, 100)
            threshold = max(5, int(quantity * random.uniform(0.1, 0.2)))
            inventory = Inventory(
                product_id=product.id,
                quantity=quantity,
                location="Main Warehouse",
                low_stock_threshold=threshold,
                last_restock_date=datetime.now()
                - timedelta(days=random.randint(1, 30)),
            )
            db.add(inventory)
            db_inventories.append(inventory)

        db.commit()

        for inventory in db_inventories:
            db.refresh(inventory)
    finally:
        db.close()

    return db_inventories


def create_customers(count: int = 20) -> list:
    db_customers = []
    db = SessionLocal()

    try:
        for _ in range(count):
            customer = Customer(
                name=fake.name(),
                email=fake.unique.email(),
                phone=fake.phone_number(),
                address=fake.address(),
            )
            db.add(customer)
            db_customers.append(customer)

        db.commit()

        for customer in db_customers:
            db.refresh(customer)
    finally:
        db.close()

    return db_customers


def create_sales(customers: list, products: list, count: int = 100) -> list:
    db_sales = []
    db = SessionLocal()

    platforms = ["Amazon", "Walmart", "Website", "eBay", "Etsy"]

    statuses = ["completed", "pending", "cancelled", "refunded"]

    try:
        for i in range(1, count + 1):
            sale_date = datetime.now() - timedelta(days=random.randint(1, 365))
            customer = random.choice(customers)
            platform = random.choice(platforms)

            status = random.choices(statuses, weights=[0.8, 0.1, 0.05, 0.05], k=1)[0]

            sale = Sale(
                order_number=f"ORD-{(sale_date.year % 100):02d}{sale_date.month:02d}-{i:04d}",
                order_date=sale_date,
                customer_id=customer.id,
                total_amount=0,
                platform=platform,
                status=status,
            )
            db.add(sale)
            db.flush()
            item_count = random.randint(1, 5)
            sale_products = random.sample(products, item_count)

            total_amount = 0
            for product in sale_products:
                quantity = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1], k=1)[0]
                discount_percent = random.uniform(0, 0.2)
                discount = round(product.price * discount_percent, 2)

                sale_item = SaleItem(
                    sale_id=sale.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=product.price,
                    discount=discount,
                )
                db.add(sale_item)
                item_total = quantity * (product.price - discount)
                total_amount += item_total

            sale.total_amount = round(total_amount, 2)
            db_sales.append(sale)

        db.commit()

        for sale in db_sales:
            db.refresh(sale)
    finally:
        db.close()

    return db_sales


def main():
    print("Creating demo data...")

    Base.metadata.create_all(bind=engine)

    print("Creating categories...")
    categories = create_categories()
    print(f"Created {len(categories)} categories.")

    print("Creating products...")
    products = create_products(categories)
    print(f"Created {len(products)} products.")

    print("Creating inventory...")
    inventories = create_inventory(products)
    print(f"Created {len(inventories)} inventory entries.")

    print("Creating customers...")
    customers = create_customers(20)
    print(f"Created {len(customers)} customers.")

    print("Creating sales...")
    sales = create_sales(customers, products, 200)
    print(f"Created {len(sales)} sales.")

    print("Demo data creation completed!")


if __name__ == "__main__":
    main()
