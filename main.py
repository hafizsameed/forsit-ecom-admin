from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from app.api.api import api_router
from app.db.session import engine, Base
from app.core.docs import tags_metadata, API_DESCRIPTION

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title=os.getenv("PROJECT_NAME", "E-commerce Admin Dashboard API"),
    description=API_DESCRIPTION,
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url=None,
    redoc_url=None,
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logging middleware
from app.core.middleware import RequestLoggingMiddleware

app.add_middleware(RequestLoggingMiddleware)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include API router
app.include_router(api_router, prefix=os.getenv("API_V1_STR", "/api"))


@app.get("/")
async def root():
    return {
        "message": "E-commerce Admin Dashboard API",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Custom Swagger UI"""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    """Custom ReDoc"""
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2.0.0/bundles/redoc.standalone.js",
    )


# Add health check endpoint
@app.get("/health", tags=["status"])
async def health_check():
    """
    Health check endpoint to verify the API is running properly.
    Returns status information about the API and its connections.
    """
    return {
        "status": "ok",
        "api_version": app.version,
        "database": "connected",  # In a real app, check the DB connection
        "timestamp": os.popen("date").read().strip(),
    }
