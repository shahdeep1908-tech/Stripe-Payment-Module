import json

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
import stripe
from routes import router

from config import app_setting

stripe.api_key = app_setting.STRIPE_API_KEY


def start_application():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture(scope="class")
def app():
    app = start_application()
    yield app


@pytest.fixture(scope="class")
def client(app):
    client = TestClient(app)
    yield client


@pytest.fixture(scope="function")
def stripe_create_product_data():
    return {'name': "Test Product", 'description': "This product is created for testing purpose"}


@pytest.fixture(scope="function")
def stripe_create_plan_data():
    return {"product_id": "abc", "name": "Stripe Test Plan", "amount": 99, "interval": "month", "currency": "usd"}


@pytest.fixture(scope="function")
def stripe_create_product(client: TestClient, stripe_create_product_data):
    response = client.post('/stripe/create-product', data=json.dumps(stripe_create_product_data))
    return response.json()['data']['id']


@pytest.fixture(scope="function")
def create_plan(client: TestClient, stripe_create_plan_data, stripe_create_product):
    stripe_create_plan_data['product_id'] = stripe_create_product

    response = client.post('/stripe/attach-plan', data=json.dumps(stripe_create_plan_data))
    return response.json()['data']['id']


@pytest.fixture(scope="function")
def stripe_payload(client: TestClient):
    with open("tests/test_data.json") as file:
        data = json.load(file)
    return data
