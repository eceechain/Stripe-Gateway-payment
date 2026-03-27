from flask import Flask, request, jsonify
from config import Config
import stripe

app = Flask(__name__)
app.config.from_object(Config)

# Set Stripe secret key
stripe.api_key = app.config["STRIPE_SECRET_KEY"]


@app.route("/")
def home():
    return "Stripe Backend API Running"


# 1. Create Payment Intent (MAIN ENDPOINT FOR POSTMAN)
@app.route("/create-payment-intent", methods=["POST"])
def create_payment_intent():
    try:
        data = request.get_json()

        amount = data.get("amount", 1000)  # amount in cents
        currency = data.get("currency", "usd")

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=["card"],
        )

        return jsonify({
            "client_secret": intent.client_secret,
            "amount": amount,
            "currency": currency
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# 2. Confirm Payment (optional for Postman testing)
@app.route("/confirm-payment", methods=["POST"])
def confirm_payment():
    try:
        data = request.get_json()

        payment_intent_id = data.get("payment_intent_id")
        payment_method = data.get("payment_method")

        intent = stripe.PaymentIntent.confirm(
            payment_intent_id,
            payment_method=payment_method
        )

        return jsonify({
            "status": intent.status,
            "id": intent.id
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)