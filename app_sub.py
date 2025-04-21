from flask import Flask, request, jsonify
from flasgger import Swagger
from subscriptions_functions import create_subscription, create_payment, complete_payment

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/', methods=['GET'])
def index():
    """
    Health check endpoint
    ---
    responses:
      200:
        description: Returns service status
    """
    return jsonify({"message": "Parking Subscription and payment  service is running"})

@app.route("/create-subscription", methods=["POST"])
def create_subscription_route():
    """
    Create a new subscription for a user
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - user_id
            - plan_type
          properties:
            user_id:
              type: string
            plan_type:
              type: string
              enum: [monthly, yearly]
    responses:
      200:
        description: Subscription created successfully
      400:
        description: User already has an active subscription
      500:
        description: Subscription created but failed to initialize payment
    """
    data = request.get_json()
    user_id = data.get("user_id")
    plan_type = data.get("plan_type")

    response, status_code = create_subscription(user_id, plan_type)
    return jsonify(response), status_code

@app.route("/create-payment", methods=["POST"])
def create_payment_route():
    """
    Initialize a new payment
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - user_id
            - sub_id
            - amount
          properties:
            user_id:
              type: string
            sub_id:
              type: integer
            amount:
              type: number
              format: float
    responses:
      200:
        description: Payment initialized
      500:
        description: Database error
    """
    data = request.get_json()
    user_id = data.get("user_id")
    sub_id = data.get("sub_id")
    amount = data.get("amount")

    response, status_code = create_payment(user_id, sub_id, amount)
    return jsonify(response), status_code

@app.route("/complete-payment", methods=["POST"])
def complete_payment_route():
    """
    Complete the latest pending payment for a user
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - user_id
          properties:
            user_id:
              type: string
    responses:
      200:
        description: Payment marked as completed
      404:
        description: No pending payments found
      500:
        description: Database error
    """
    data = request.get_json()
    user_id = data.get("user_id")

    response, status_code = complete_payment(user_id)
    return jsonify(response), status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
