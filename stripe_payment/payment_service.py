import uuid

import stripe


async def checkout_payment_session(request, app):
    data = await request.json()

    if not app.state.stripe_customer_id:
        customer = stripe.Customer.create(
            description=f'cust-{uuid.uuid4()}'
        )
        app.state.stripe_customer_id = customer['id']
    checkout_session = stripe.checkout.Session.create(
        customer=app.state.stripe_customer_id,
        success_url="http://localhost:8000/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://localhost:8000/cancel",
        payment_method_types=["card"],
        mode="subscription",
        line_items=[{
            "price": data["priceId"],
            "quantity": 1
        }],
    )
    return {"sessionId": checkout_session['id']}


async def customer_service_portal(app):
    session = stripe.billing_portal.Session.create(
        customer=app.state.stripe_customer_id,
        return_url="http://localhost:8000/subscribe"
    )
    return {"url": session.url}
