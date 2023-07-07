## Stripe Payment Module
This module provides integration with the Stripe payment gateway, allowing you to easily accept online payments in your application.

## Features
- Seamless integration with Stripe API for processing Products and Plans
- Support for various payment methods (credit cards, digital wallets, etc.)
- Simplified checkout flow with FastAPI jinja2 templating.
- Automated handling of payment-related events (success, failure, etc.)
- Secure and PCI-compliant payment processing for subscription based payments

## Requirements
- Python 3.7+
- FastAPI framework
- Stripe API keys (test and live)

## Installation
1. Clone the repository:
```shell
https://gitlab.inexture.com/deep.inexture/stripe-payment-module
```
2. Install the required dependencies:
```shell
pip install -r requirements.txt
```
3. Configure Stripe API keys:
- Sign up for a Stripe account at https://stripe.com if you haven't already.
- Create a new project and obtain the test and live API keys from the Stripe dashboard.
- Set the API keys as environment variables or update the configuration file with the keys.

4. Start the application:
```commandline
python main.py
```

## Configuration
The module supports configuration via environment variables. Create a .env file in the project root directory and set the following variables:
```python
STRIPE_API_KEY=<your-test-api-key>
STRIPE_PUB_KEY=<your-test-pub-key>
STRIPE_WEBHOOK_SECRET=<your-webhook-secret-key>
```

## Usage
Add the STRIPE_PUB_KEY to script.js file as it is a public key to communicate with Stripe dashboard.
```javascript
const stripe = Stripe("pk_key_xxx");
```

## License
```text
Feel free to modify and tailor it according to your specific requirements and project structure.
```