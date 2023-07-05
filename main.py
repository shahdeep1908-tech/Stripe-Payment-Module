import stripe
import uvicorn
from fastapi import FastAPI
from routes import router as api_routes

from config import app_setting
from common import constants

app = FastAPI(title=constants.PROJECT_NAME,
              docs_url=constants.DOCS_URL_PATH,
              redoc_url=constants.REDOC_URL_PATH)

"""Initialized routes.py file as api_router"""
app.include_router(api_routes)

# StripeKey initializing
# stripe.api_key = app_setting.STRIPE_API_KEY

if __name__ == '__main__':
    uvicorn.run(
        app_setting.FASTAPI_APP,
        host=app_setting.HOST_URL,
        port=app_setting.HOST_PORT,
        log_level=app_setting.FASTAPI_LOG_LEVEL,
        reload=app_setting.FASTAPI_APP_RELOAD
    )
