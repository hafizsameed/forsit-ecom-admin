# E-commerce Admin Dashboard API

A back-end API to power a web admin dashboard for e-commerce managers. This API provides detailed insights into sales, revenue, and inventory status, as well as allows new product registration.

## Features

### Sales Status
- Retrieve, filter, and analyze sales data
- Analyze revenue on a daily, weekly, monthly, and annual basis
- Compare revenue across different periods and categories
- Provide sales data by date range, product, and category

### Inventory Management
- View current inventory status, including low stock alerts
- Update inventory levels and track changes over time
- Record inventory history

### Product Management
- Create, update, and delete products
- Categorize products for better organization
- Track product information including SKU and pricing

### Dashboard Analytics
- Summary dashboard with key performance metrics
- Top-selling products overview
- Sales platform distribution analysis
- Period-over-period comparison

### Additional Features
- Request logging middleware for monitoring
- Rate limiting for API protection
- Health check endpoint for monitoring
- Export sample data for frontend development

## Tech Stack

- Python 3.8+
- FastAPI - High-performance web framework
- SQLAlchemy - SQL toolkit and ORM
- MySQL - Relational database
- Pydantic - Data validation and settings management
- Alembic - Database migration tool
- Faker - Demo data generation

## Setup Instructions

### Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/ecommerce-dashboard-api.git
   cd ecommerce-dashboard-api
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure the .env file:
   ```
   # Example .env file
   DATABASE_URL=mysql+pymysql://username:password@localhost/ecommerce_dashboard
   API_V1_STR=/api
   PROJECT_NAME="E-commerce Admin Dashboard API"
   ```
   Update the DATABASE_URL with your MySQL credentials.

5. Create the database:
   ```
   mysql -u username -p
   CREATE DATABASE ecommerce_dashboard;
   exit
   ```

6. Run the database migrations (if using Alembic):
   ```
   alembic upgrade head
   ```
   
   Or let the application create the tables:
   ```
   uvicorn main:app --reload
   ```

7. Generate demo data:
   ```
   python scripts/create_demo_data.py
   ```
   
8. Export sample data for frontend development (optional):
   ```
   python scripts/export_sample_data.py
   ```
   
9. Run the application using the convenience script:
   ```
   ./run.sh
   ```
   
   Or with uvicorn directly:
   ```
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Docker Installation (Alternative)

You can also run the application using Docker:

1. Make sure you have Docker and Docker Compose installed

2. Build and run the containers:
   ```
   docker-compose up --build
   ```
   
3. The API will be accessible at http://localhost:8000

4. Generate demo data:
   ```
   docker-compose exec api python scripts/create_demo_data.py
   ```

5. To stop the containers:
   ```
   docker-compose down
   ```

8. Start the application:
   ```
   uvicorn main:app --reload
   ```

9. Open your browser and navigate to:
   ```
   http://localhost:8000/docs
   ```

## API Endpoints

All endpoints are prefixed with `/api/v1` to support API versioning. This allows future API versions (like `/api/v2`) to be created without breaking existing clients. The version prefix is configured in the `.env` file.

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /api/v1/categories/ | Get all categories |
| GET    | /api/v1/categories/{category_id} | Get a specific category |
| POST   | /api/v1/categories/ | Create a new category |
| PUT    | /api/v1/categories/{category_id} | Update a category |
| DELETE | /api/v1/categories/{category_id} | Delete a category |

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /api/v1/products/ | Get all products |
| GET    | /api/v1/products/{product_id} | Get a specific product |
| POST   | /api/v1/products/ | Create a new product |
| PUT    | /api/v1/products/{product_id} | Update a product |
| DELETE | /api/v1/products/{product_id} | Delete a product |

### Inventory

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /api/v1/inventory/ | Get all inventory entries |
| GET    | /api/v1/inventory/{inventory_id} | Get a specific inventory entry |
| GET    | /api/v1/inventory/product/{product_id} | Get inventory for a product |
| POST   | /api/v1/inventory/ | Create a new inventory entry |
| PUT    | /api/v1/inventory/{inventory_id} | Update an inventory entry |
| GET    | /api/v1/inventory/{inventory_id}/history | Get history for an inventory |
| GET    | /api/v1/inventory/low-stock | Get low stock alerts |

### Customers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /api/v1/customers/ | Get all customers |
| GET    | /api/v1/customers/{customer_id} | Get a specific customer |
| POST   | /api/v1/customers/ | Create a new customer |
| PUT    | /api/v1/customers/{customer_id} | Update a customer |

### Sales

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /api/v1/sales/ | Get all sales |
| GET    | /api/v1/sales/{sale_id} | Get a specific sale |
| GET    | /api/v1/sales/order/{order_number} | Get a sale by order number |
| POST   | /api/v1/sales/ | Create a new sale |
| PUT    | /api/v1/sales/{sale_id} | Update a sale |

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /api/v1/analytics/sales | Get sales analytics |
| POST   | /api/v1/analytics/revenue | Get revenue analytics |
| POST   | /api/v1/analytics/inventory | Get inventory analytics |
| POST   | /api/v1/analytics/revenue/compare | Compare revenue between periods |

### Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /api/v1/dashboard/summary | Get summary of key metrics |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /health | Health check endpoint |
| GET    | /docs | Interactive API documentation (Swagger UI) |
| GET    | /redoc | Alternative API documentation (ReDoc) |

## Database Schema

The database consists of the following tables:

### categories
- `id` - Primary key
- `name` - Category name (unique)
- `description` - Category description
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

### products
- `id` - Primary key
- `name` - Product name
- `description` - Product description
- `sku` - Stock Keeping Unit (unique)
- `price` - Product price
- `category_id` - Foreign key to categories table
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

### inventory
- `id` - Primary key
- `product_id` - Foreign key to products table
- `quantity` - Current stock quantity
- `location` - Storage location
- `low_stock_threshold` - Threshold for low stock alerts
- `last_restock_date` - Date of last restock
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

### inventory_history
- `id` - Primary key
- `inventory_id` - Foreign key to inventory table
- `previous_quantity` - Previous stock quantity
- `new_quantity` - New stock quantity
- `change_reason` - Reason for the change
- `created_at` - Creation timestamp

### customers
- `id` - Primary key
- `name` - Customer name
- `email` - Customer email (unique)
- `phone` - Customer phone
- `address` - Customer address
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

### sales
- `id` - Primary key
- `order_number` - Order number (unique)
- `order_date` - Date of the order
- `customer_id` - Foreign key to customers table
- `total_amount` - Total order amount
- `platform` - Sales platform (e.g., Amazon, Walmart)
- `status` - Order status
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

### sale_items
- `id` - Primary key
- `sale_id` - Foreign key to sales table
- `product_id` - Foreign key to products table
- `quantity` - Quantity sold
- `unit_price` - Unit price at the time of sale
- `discount` - Discount applied
- `created_at` - Creation timestamp

## Entity Relationships

1. A `category` can have multiple `products`
2. A `product` belongs to one `category`
3. A `product` has one `inventory` entry
4. An `inventory` entry can have multiple `inventory_history` records
5. A `customer` can have multiple `sales`
6. A `sale` belongs to one `customer`
7. A `sale` can have multiple `sale_items`
8. A `sale_item` belongs to one `sale` and one `product`

## Demo Data

The application includes a script to generate demo data for testing and evaluation. This data includes:
- 8 product categories
- 40 products (5 per category)
- Inventory records for all products
- 20 customers
- 200 sales records with items

The demo data includes sales spread over the last year on various platforms (Amazon, Walmart, etc.) to facilitate analytics testing.