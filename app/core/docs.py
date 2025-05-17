tags_metadata = [
    {
        "name": "categories",
        "description": "Operations with product categories. Categories organize products into logical groups.",
    },
    {
        "name": "products",
        "description": "Manage product information including names, descriptions, prices, and SKUs.",
    },
    {
        "name": "inventory",
        "description": "Track product inventory levels, restock dates, and low stock alerts.",
    },
    {
        "name": "customers",
        "description": "Maintain customer information for orders and sales analysis.",
    },
    {
        "name": "sales",
        "description": "Process and retrieve sales data including orders, line items, and pricing.",
    },
    {
        "name": "analytics",
        "description": "Analyze sales, revenue, and inventory data with various filters and time periods.",
    },
]

API_DESCRIPTION = """
E-commerce Admin Dashboard API

This API powers an admin dashboard for e-commerce managers, providing:

## Key Features

### Sales and Revenue Analytics
* Daily, weekly, monthly, and annual revenue analysis
* Sales data filtering by date range, product, and category
* Revenue comparison across different time periods

### Inventory Management
* Current stock levels and low stock alerts
* Inventory history tracking
* Stock level updates

### Product Management
* Complete product CRUD operations
* Category organization
* SKU and pricing management

## Authentication
API endpoints require authentication (to be implemented).

## Rate Limiting
API requests are subject to rate limiting (to be implemented).
"""
